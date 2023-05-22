from src.api.handlers.admin.council import StartOnlineVotingHandler
from src.api.middlewares.session import session
from src.orm.repositories import (
    DepartmentAdminRepository,
    PollRepository,
    CouncilRepository,
    CouncilStatusRepository,
    PollStatusRepository,
    VoteRepository,
)
from src.services.scheduler import scheduler


@scheduler.task(once=True)
@session(commit=True)
async def start_online_voting_task(council_id: int) -> None:
    handler = StartOnlineVotingHandler(
        CouncilRepository(),
        PollRepository(),
        DepartmentAdminRepository(),
        CouncilStatusRepository(),
        PollStatusRepository(),
        VoteRepository(),
        check_user_info=False,
    )
    await handler.handle(council_id)
