from io import BytesIO, StringIO
from typing import Union, Optional, Callable

import streamlit as st

from src.config import ADMIN_USERNAME
from src.submissions.submissions_manager import SubmissionManager, SingleParticipantSubmissions


class SubmissionSidebar:
    def __init__(self, username: str, submission_manager: SubmissionManager,
                 submission_file_extension: Optional[str] = None,
                 submission_validator: Optional[Callable[[Union[StringIO, BytesIO]], bool]] = None):
        self.username = username
        self.submission_manager = submission_manager
        self.submission_file_extension = submission_file_extension
        self.submission_validator = submission_validator
        self.participant: SingleParticipantSubmissions = None
        self.file_uploader_key = f"file upload {username}"

    def init_participant(self):
        self.submission_manager.add_participant(self.username, exists_ok=True)
        self.participant = self.submission_manager.get_participant(self.username)

    def run_submission(self):
        st.sidebar.title(f"Hello {self.username}!")
        if self.username != ADMIN_USERNAME:
            st.sidebar.markdown("## Submit Your Predictions Here :fire:")
            self.submit()

    def submit(self):
        file_extension_suffix = f" (.{self.submission_file_extension})" if self.submission_file_extension else None
        submission_io_stream = st.sidebar.file_uploader("Upload your submission csv" + file_extension_suffix,
                                                        type=self.submission_file_extension,
                                                        key=self.file_uploader_key)
        ipynb = st.sidebar.text_input('Notebook URL')
        parameter_count = st.sidebar.text_input('Parameter Count')
        if st.sidebar.button('Submit'):
            try:
                parameter_count = int(parameter_count)
            except ValueError:
                st.sidebar.error('Invalid parameter value.')
                return

            if submission_io_stream is None or type(parameter_count) != int or len(ipynb) == 0:
                st.sidebar.error('Please complete every field.')
            else:
                submission_failed = True
                with st.spinner('Uploading your submission...'):
                    if self.submission_validator is None or self.submission_validator(submission_io_stream):
                        self._upload_submission(submission_io_stream, parameter_count, ipynb)
                        submission_failed = False
                if submission_failed:
                    st.sidebar.error("Upload failed. The submission file is not valid.")
                else:
                    st.sidebar.success("Upload successful!")

    def _upload_submission(self, io_stream: Union[BytesIO, StringIO], parameter_count: Optional[str] = None, ipynb: Optional[str] = None):
        self.init_participant()
        self.participant.add_submission(io_stream, parameter_count, self.submission_file_extension, ipynb)
