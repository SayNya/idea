from fastapi import Depends

from src.orm.repositories import VoteRepository


class ResponsibleVotesCountHandler:
    def __init__(
        self,
        vote_repository: VoteRepository = Depends(),
    ):
        self.vote_repository = vote_repository

    async def handle(self, council_id: int, poll_number: int) -> dict:
        votes_count = await self.vote_repository.count_votes_for_poll(
            council_id, poll_number
        )
        return {"votesCount": votes_count}
