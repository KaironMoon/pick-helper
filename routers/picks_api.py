from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel

from dao.database import get_db

router = APIRouter(
    prefix="",
    tags=["api/v1/picks"],
    responses={404: {"description": "Not found"}},
)


class PickResponse(BaseModel):
    seq: int
    prev_picks: str
    next_pick: str | None


class PickSetRequest(BaseModel):
    prev_picks: str
    next_pick: str


class PickAddRequest(BaseModel):
    prev_picks: str
    next_pick: str | None = None


@router.get("/seq/{seq}", response_model=PickResponse)
async def get_pick_by_seq(
    seq: int,
    skip_filled: bool = False,
    direction: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """seq로 pick 조회. skip_filled=true면 next_pick이 비어있는 다음 seq 반환. direction=next/prev면 해당 방향으로 가장 가까운 seq 반환"""
    if skip_filled:
        query = text("""
            SELECT seq, prev_picks, next_pick
            FROM picks
            WHERE seq >= :seq AND next_pick IS NULL
            ORDER BY seq
            LIMIT 1
        """)
    elif direction == "next":
        query = text("""
            SELECT seq, prev_picks, next_pick
            FROM picks
            WHERE seq > :seq
            ORDER BY seq ASC
            LIMIT 1
        """)
    elif direction == "prev":
        query = text("""
            SELECT seq, prev_picks, next_pick
            FROM picks
            WHERE seq < :seq
            ORDER BY seq DESC
            LIMIT 1
        """)
    else:
        query = text("""
            SELECT seq, prev_picks, next_pick
            FROM picks
            WHERE seq = :seq
        """)

    result = await db.execute(query, {"seq": seq})
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Pick not found")

    return PickResponse(seq=row.seq, prev_picks=row.prev_picks, next_pick=row.next_pick)


@router.get("/pattern/{prev_picks}", response_model=PickResponse)
async def get_pick_by_pattern(
    prev_picks: str,
    db: AsyncSession = Depends(get_db)
):
    """prev_picks 패턴으로 pick 조회"""
    query = text("""
        SELECT seq, prev_picks, next_pick
        FROM picks
        WHERE prev_picks = :prev_picks
    """)

    result = await db.execute(query, {"prev_picks": prev_picks})
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Pick not found")

    return PickResponse(seq=row.seq, prev_picks=row.prev_picks, next_pick=row.next_pick)


@router.post("/set", response_model=PickResponse)
async def set_pick(
    request: PickSetRequest,
    db: AsyncSession = Depends(get_db)
):
    """prev_picks의 next_pick 설정. 있으면 수정, 없으면 추가"""
    query = text("""
        INSERT INTO picks (prev_picks, next_pick)
        VALUES (:prev_picks, :next_pick)
        ON CONFLICT (prev_picks)
        DO UPDATE SET next_pick = :next_pick
        RETURNING seq, prev_picks, next_pick
    """)

    result = await db.execute(query, {
        "prev_picks": request.prev_picks,
        "next_pick": request.next_pick
    })
    await db.commit()
    row = result.fetchone()

    return PickResponse(seq=row.seq, prev_picks=row.prev_picks, next_pick=row.next_pick)


@router.delete("/pattern/{prev_picks}/next", response_model=PickResponse)
async def delete_next_pick(
    prev_picks: str,
    db: AsyncSession = Depends(get_db)
):
    """prev_picks의 next_pick 삭제 (NULL로 설정)"""
    query = text("""
        UPDATE picks
        SET next_pick = NULL
        WHERE prev_picks = :prev_picks
        RETURNING seq, prev_picks, next_pick
    """)

    result = await db.execute(query, {"prev_picks": prev_picks})
    await db.commit()
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Pick not found")

    return PickResponse(seq=row.seq, prev_picks=row.prev_picks, next_pick=row.next_pick)


@router.delete("/pattern/{prev_picks}")
async def delete_pattern(
    prev_picks: str,
    db: AsyncSession = Depends(get_db)
):
    """패턴 자체를 삭제"""
    query = text("""
        DELETE FROM picks
        WHERE prev_picks = :prev_picks
        RETURNING seq
    """)

    result = await db.execute(query, {"prev_picks": prev_picks})
    await db.commit()
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Pick not found")

    return {"message": "Pattern deleted", "seq": row.seq}


@router.post("/add", response_model=PickResponse)
async def add_pattern(
    request: PickAddRequest,
    db: AsyncSession = Depends(get_db)
):
    """새 패턴 추가"""
    query = text("""
        INSERT INTO picks (prev_picks, next_pick)
        VALUES (:prev_picks, :next_pick)
        RETURNING seq, prev_picks, next_pick
    """)

    try:
        result = await db.execute(query, {
            "prev_picks": request.prev_picks,
            "next_pick": request.next_pick
        })
        await db.commit()
        row = result.fetchone()
        return PickResponse(seq=row.seq, prev_picks=row.prev_picks, next_pick=row.next_pick)
    except Exception:
        raise HTTPException(status_code=400, detail="Pattern already exists")
