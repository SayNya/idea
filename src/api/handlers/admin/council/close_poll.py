# from typing import Union
#
# from fastapi import Depends
#
# from src.api.handlers.responsible.change_status import ChangeIdeaStatusHandler
# from src.api.handlers.responsible.council.acceptance.end_council import (
#     ResponsibleEndCouncilHandler,
# )
# from src.exceptions.exceptions.application import ApplicationException
# from src.exceptions.exceptions.bad_request import BadRequestException
# from src.exceptions.exceptions.not_found import NotFoundException
# from src.orm.repositories import (
#     CouncilResultsRepository,
#     DepartmentAdminsRepository,
#     IdeaRepository,
#     PollRepository,
# )
# from src.orm.schemas.enum import (
#     CouncilResultAttributeKeysEnum,
#     IdeaStatusCodeEnum,
#     PollStatusesEnum,
# )
# from src.orm.schemas.requests.responsible import ResponsibleChangeStatusRequest
# from src.schemas.responses.auth import UserAuthResponse
# from src.orm.schemas.responses.responsible.council import CompleteCouncilResponse
#
#
# class ClosePollHandler:
#     def __init__(
#         self,
#         poll_repository: PollRepository = Depends(),
#         council_results_repository: CouncilResultsRepository = Depends(),
#         change_idea_status_handler: ChangeIdeaStatusHandler = Depends(),
#         responsible_end_council_handler: ResponsibleEndCouncilHandler = Depends(),
#         idea_repository: IdeaRepository = Depends(),
#         department_admins_repository: DepartmentAdminsRepository = Depends(),
#     ):
#         self.poll_repository = poll_repository
#         self.council_results_repository = council_results_repository
#         self.change_idea_status_handler = change_idea_status_handler
#         self.end_council_handler = responsible_end_council_handler
#         self.idea_repository = idea_repository
#         self.department_admins_repository = department_admins_repository
#
#     status_to_key_mapping = {
#         IdeaStatusCodeEnum.ACCEPTED: CouncilResultAttributeKeysEnum.ACCEPTED_IDEAS,
#         IdeaStatusCodeEnum.UPDATING: CouncilResultAttributeKeysEnum.TO_UPDATING_IDEAS,
#         IdeaStatusCodeEnum.DECLINED: CouncilResultAttributeKeysEnum.DECLINED_IDEAS,
#     }
#
#     async def handle(
#         self,
#         council_id: int,
#         poll_number: int,
#         change_status_request: ResponsibleChangeStatusRequest,
#         user_info: UserAuthResponse,
#     ) -> Union[dict, CompleteCouncilResponse]:
#         department_responsible = (
#             await self.department_admins_repository.get_department_of_responsible(
#                 user_info.id
#             )
#         )
#         if not department_responsible:
#             raise ApplicationException(detail="user is not department_responsible")
#         # validate status
#         if change_status_request.status not in [
#             IdeaStatusCodeEnum.ACCEPTED,
#             IdeaStatusCodeEnum.UPDATING,
#             IdeaStatusCodeEnum.DECLINED,
#         ]:
#             raise BadRequestException(detail="wrong status")
#         # check existing of council
#         poll = await self.poll_repository.find_with_council(council_id, poll_number)
#         if (
#             not poll
#             or poll.council.department.id != department_responsible.department_id
#         ):
#             raise NotFoundException(detail="poll not found")
#         # check council status
#
#         if poll.status != PollStatusesEnum.ENDED:
#             raise BadRequestException(
#                 detail="can't close poll for council with current status"
#             )
#         # check council fpr ended polls
#         ended_polls = await self.poll_repository.find_by_council_id_and_statuses(
#             poll.council.id, [PollStatusesEnum.ENDED]
#         )
#         # close poll
#         await self.poll_repository.update(
#             ended_polls[0].id, {"status": PollStatusesEnum.CLOSED}
#         )
#         # mark ideas as participant of council
#         if change_status_request.status != IdeaStatusCodeEnum.UPDATING:
#             await self.idea_repository.update(
#                 ended_polls[0].idea_id, {"if_accept_council": True}
#             )
#         # invoke handler for change idea status
#         await self.change_idea_status_handler.handle(
#             ended_polls[0].idea_id, change_status_request, user_info
#         )
#
#         # save results
#         attribute_key = self.status_to_key_mapping.get(change_status_request.status)
#         result = await self.council_results_repository.find_by_council_id_and_key(
#             poll.council.id,
#             attribute_key,
#         )
#         await self.council_results_repository.update_result_by_council_id_and_key(
#             poll.council.id, attribute_key, f"{(int(result.result) + 1)}"
#         )
#
#         blocked_polls = await self.poll_repository.find_by_council_id_and_statuses(
#             poll.council.id, [PollStatusesEnum.BLOCKED]
#         )
#         if blocked_polls:
#             # open next poll
#             await self.poll_repository.update(
#                 blocked_polls[0].id, {"status": PollStatusesEnum.OPENED}
#             )
#             return {}
#         else:
#             # or close council
#             return await self.end_council_handler.handle(poll.council.id, user_info)
