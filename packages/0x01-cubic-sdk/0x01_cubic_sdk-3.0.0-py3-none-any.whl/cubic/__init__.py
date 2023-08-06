"""Cubic SDK"""

__all__ = ['Change', 'Cubic', 'Hash', 'Item', 'RemovedItem', 'Version', 'VersionData']

from dataclasses import dataclass
from itertools import islice
from hashlib import sha3_256
import struct
from typing import Dict, Iterable, List, Mapping, Optional, Set, Tuple, Union

import msgpack
import requests


Hash = bytes


@dataclass(frozen=True)
class Item:
    meta: bytes
    blocks: List[Hash]


@dataclass(frozen=True)
class RemovedItem:
    def __bool__(self):
        return False


Change = Union[Item, RemovedItem]


@dataclass(frozen=True)
class Version:
    checksum: bytes
    timestamp: int
    timestamp_ns: int


@dataclass(frozen=True)
class VersionData:
    checksum: bytes
    timestamp: int
    timestamp_ns: int
    items: Dict[bytes, Item]


def _validate(version: VersionData) -> None:
    hash = sha3_256(struct.pack('>qII', version.timestamp, version.timestamp_ns, len(version.items)))
    for path in sorted(version.items):
        item = version.items[path]
        hash.update(struct.pack('>III', len(path), len(item.meta), len(item.blocks)))
        hash.update(path)
        hash.update(item.meta)
        for h in item.blocks:
            hash.update(h)
    if hash.digest() != version.checksum:
        raise ValueError('VersionData validation failed')


ENDPOINT = 'https://api.cubic.0x01.me'


class Cubic:

    class Error(Exception):
        pass

    def __init__(self, tree, token, endpoint=ENDPOINT, session=None, timeout=60):
        self._tree = tree
        self._endpoint = endpoint
        self._session = session or requests.Session()
        self._session.auth = tree, token
        self._timeout = timeout
        self._limits = self._call('/v3/limits')

    def _call(self, api, payload=None):
        r = self._session.post(self._endpoint + api, data=msgpack.packb(payload), timeout=self._timeout)
        if not r.ok:
            raise self.Error(r)
        return msgpack.unpackb(r.content)

    def dedup_blocks(self, hashes: Iterable[Hash]) -> Set[Hash]:
        """Filter blocks that need to be uploaded."""
        hashes = list(hashes)
        result = set()
        limit = self._limits['dedupBlocks/count']
        for i in range(0, len(hashes), limit):
            result.update(self._call('/v3/dedupBlocks', hashes[i:i+limit]))
        return result

    def put_blocks(self, blocks: Iterable[bytes]) -> None:
        """Upload all blocks.

        You may want to use dedup_put_blocks instead.
        """
        buffer = []
        size = 0
        limit_count = self._limits['putBlocks/count']
        limit_size = self._limits['putBlocks/size']
        for i in blocks:
            if len(buffer) + 1 > limit_count or size + len(i) > limit_size:
                if buffer:
                    self._call('/v3/putBlocks', buffer)
                    buffer = []
                    size = 0
            buffer.append(i)
            size += len(i)
        self._call('/v3/putBlocks', buffer)

    def dedup_put_blocks(self, blocks: Mapping[Hash, bytes]) -> None:
        """Only upload necessary blocks."""
        self.put_blocks(blocks[i] for i in self.dedup_blocks(blocks))

    def put_block(self, block: bytes) -> None:
        """Upload one block."""
        self._call('/v3/putBlocks', [block])

    def get_blocks(self, hashes: Iterable[Hash]) -> Dict[Hash, bytes]:
        """Download all blocks."""
        hashes = set(hashes)
        result = {}
        limit = self._limits['getBlocks/count']
        while hashes:
            buffer = list(islice(hashes, limit))
            for k, v in self._call('/v3/getBlocks', buffer).items():
                hashes.discard(k)
                result[k] = v
        return result

    def get_block(self, hash: Hash) -> bytes:
        """Download one block."""
        return self._call('/v3/getBlocks', [hash])[hash]

    def list_versions(self) -> List[Version]:
        """List all versions (most recent version last)."""
        return [Version(*i) for i in self._call('/v3/listVersions')]

    def diff_versions(self, from_: Union[None, Version, VersionData], to: Version) -> Dict[bytes, Change]:
        """Get changes between two versions."""
        def f(x: Optional[Iterable]) -> Change:
            return Item(*x) if x else RemovedItem()
        payload = (from_.checksum if from_ else None), to.checksum
        return {k: f(v) for k, v in self._call('/v3/diffVersions', payload).items()}

    def get_version(self, version: Version, base: Optional[VersionData] = None) -> VersionData:
        """Get items of a version.

        If base is provided, only download changes between two versions."""
        items = base.items.copy() if base else {}
        for k, v in self.diff_versions(base, version).items():
            if v:
                items[k] = v
            else:
                del items[k]
        result = VersionData(version.checksum, version.timestamp, version.timestamp_ns, items)
        _validate(result)
        return result

    def update_version(self, changes: Mapping[bytes, Change], base: Optional[VersionData] = None) -> VersionData:
        """Create a new version using an old version and changes."""
        def f(x: Change) -> Optional[Tuple]:
            return (x.meta, x.blocks) if x else None
        payload = (base.checksum if base else None), {k: f(v) for k, v in changes.items()}
        result = self._call('/v3/updateVersion', payload)
        _validate(result)
        return result
