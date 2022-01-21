import uuid

import pytest

from main.redis import *


@pytest.mark.asyncio
async def test_channels_sane():
    name = 'test-channel'
    reader = await RedisReadOnlyChannel.create(name=name)
    await reader.close()
    writer = await RedisWriteOnlyChannel.create(name=name)
    await writer.close()


@pytest.mark.asyncio
async def test_channels_read_write():
    name = 'test-channel'
    expected_data = {'marker': uuid.uuid4().hex}
    actual_data = None

    r_chan = await RedisReadOnlyChannel.create(name=name)
    w_chan = await RedisWriteOnlyChannel.create(name=name)

    try:
        async def writer():
            res = await w_chan.write(expected_data)
            assert res is True, 'Write to channel has problems'

        async def reader():
            nonlocal actual_data
            success, res = await r_chan.read(timeout=1)
            actual_data = res

        done, pending = await asyncio.wait([reader(), writer()], timeout=3)
        assert len(done) == 2, 'Not all async workers have done in limited time!'
        assert expected_data == actual_data
    finally:
        await r_chan.close()
        await w_chan.close()


@pytest.mark.asyncio
async def test_channels_read_write_sequence():
    name = 'test-channel'
    expected_sequence = [
        {'marker': uuid.uuid4().hex},
        {'marker': uuid.uuid4().hex},
        {'marker': uuid.uuid4().hex}
    ]
    actual_sequence = []
    r_chan = await RedisReadOnlyChannel.create(name=name)
    w_chan = await RedisWriteOnlyChannel.create(name=name)

    async def writer():
        for msg in expected_sequence:
            res = await w_chan.write(msg)
            assert res is True, 'Write to channel has problems'

    async def reader():
        nonlocal actual_sequence
        while True:
            success, res = await r_chan.read(timeout=None)
            actual_sequence.append(res)

    try:
        done, pending = await asyncio.wait([reader(), writer()], timeout=1)
        assert len(done) == 1, 'Data producer steel working'
        assert len(pending) == 1, 'Data consumer unexpected done, Check timeout errors'
        assert expected_sequence == actual_sequence
    finally:
        await r_chan.close()
        await w_chan.close()


@pytest.mark.asyncio
async def test_channels_closing_behaviour_1():
    name = 'test-channel'

    r_chan = await RedisReadOnlyChannel.create(name=name)
    w_chan = await RedisWriteOnlyChannel.create(name=name)

    await r_chan.close()
    with pytest.raises(ChannelIsClosedError):
        await r_chan.read(timeout=1)

    await w_chan.close()
    with pytest.raises(ChannelIsClosedError):
        await w_chan.write({})


@pytest.mark.asyncio
async def test_channels_closing_behaviour_2():
    name = 'test-channel'
    expected_sequence = [
        {'marker': uuid.uuid4().hex},
        {'marker': uuid.uuid4().hex},
        {'marker': uuid.uuid4().hex}
    ]
    actual_sequence = []
    r_chan = await RedisReadOnlyChannel.create(name=name)
    w_chan = await RedisWriteOnlyChannel.create(name=name)

    async def writer():
        for msg in expected_sequence:
            res = await w_chan.write(msg)
            assert res is True, 'Write to channel has problems'
        await w_chan.close()

    async def reader():
        nonlocal actual_sequence
        while True:
            success, res = await r_chan.read(timeout=None)
            if success:
                actual_sequence.append(res)
            else:
                break

    try:
        done, pending = await asyncio.wait([reader(), writer()], timeout=1)
        assert len(done) == 2
        assert expected_sequence == actual_sequence
    finally:
        await r_chan.close()
        await w_chan.close()


@pytest.mark.asyncio
async def test_channels_read_timeout():
    name = 'test-channel'

    r_chan = await RedisReadOnlyChannel.create(name=name)

    try:
        with pytest.raises(ReadWriteTimeoutError):
            await r_chan.read(timeout=1)
    finally:
        await r_chan.close()


@pytest.mark.asyncio
async def test_transmit_bytes():
    name = 'test_transmit_bytes'
    r_chan = await RedisReadOnlyChannel.create(name=name)
    w_chan = await RedisWriteOnlyChannel.create(name=name)
    await w_chan.write(b'Hello')
    _, value = await r_chan.read(3)
    assert value == b'Hello'
