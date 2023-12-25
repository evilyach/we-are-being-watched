from app.database.session import session_manager


async def add[T](obj: T) -> T:
    async with session_manager.session() as session:
        session.add(obj)

        await session.commit()
        await session.refresh(obj)

        return obj


async def add_all[T](objs: list[T]) -> list[T]:
    async with session_manager.session() as session:
        session.add_all(objs)

        await session.commit()

        for obj in objs:
            await session.refresh(obj)

        return objs
