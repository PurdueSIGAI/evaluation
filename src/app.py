import sys, pathlib

import streamlit as st

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from src.common.session_state import get_session_state
from src.login.login import Login
from src.login.username_password_manager import UsernamePasswordManagerArgon2
from src.submissions.submissions_manager import SubmissionManager
from src.config import SUBMISSIONS_DIR, EVALUATOR_CLASS, EVALUATOR_KWARGS, PASSWORDS_DB_FILE, ARGON2_KWARGS, \
    ALLOWED_SUBMISSION_FILE_EXTENSION, MAX_NUM_USERS, ADMIN_USERNAME
from src.submissions.submission_sidebar import SubmissionSidebar
from src.evaluation.evaluator import Evaluator
from src.display.leaderboard import Leaderboard
from src.display.personal_progress import PersonalProgress
from src.common.css_utils import set_block_container_width


def get_login() -> Login:
    password_manager = UsernamePasswordManagerArgon2(PASSWORDS_DB_FILE, **ARGON2_KWARGS)
    return Login(password_manager, MAX_NUM_USERS)


@st.cache(allow_output_mutation=True)
def get_submission_manager():
    return SubmissionManager(SUBMISSIONS_DIR)


@st.cache(allow_output_mutation=True)
def get_submission_sidebar(username: str) -> SubmissionSidebar:
    return SubmissionSidebar(username, get_submission_manager(),
                             submission_validator=get_evaluator().validate_submission,
                             submission_file_extension=ALLOWED_SUBMISSION_FILE_EXTENSION)


@st.cache(allow_output_mutation=True)
def get_evaluator() -> Evaluator:
    return EVALUATOR_CLASS(**EVALUATOR_KWARGS)


@st.cache(allow_output_mutation=True)
def get_leaderboard() -> Leaderboard:
    return Leaderboard(get_submission_manager(), get_evaluator())


@st.cache(allow_output_mutation=True)
def get_personal_progress(username: str) -> PersonalProgress:
    return PersonalProgress(get_submission_manager().get_participant(username), get_evaluator())


@st.cache
def get_users_without_admin():
    return [user for user in get_submission_manager().participants.keys() if user != ADMIN_USERNAME]


def admin_display_personal_progress():
    selected_user = st.sidebar.selectbox('Select user to view',
                                         get_users_without_admin())
    if selected_user is not None:
        get_personal_progress(selected_user).show_progress(progress_placeholder)


login = get_session_state(login=get_login()).login
login.init()
leaderboard_placeholder = st.empty()
progress_placeholder = st.empty()

if login.run_and_return_if_access_is_allowed() and not login.has_user_signed_out():
    username = login.get_username()
    get_submission_sidebar(username).run_submission()
    get_leaderboard().display_leaderboard(username, leaderboard_placeholder)
    if get_submission_manager().participant_exists(username) and username != ADMIN_USERNAME:
        get_personal_progress(username).show_progress(progress_placeholder)
    if username == ADMIN_USERNAME:
        admin_display_personal_progress()
else:
    get_leaderboard().display_leaderboard('', leaderboard_placeholder)
