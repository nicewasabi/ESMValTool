"""Downloader for the Climate Data Store"""

import os
import ftplib
import logging
import subprocess

from progressbar import ProgressBar, Bar, DataSize, ETA,\
    FileTransferSpeed, Percentage

logger = logging.getLogger(__name__)


class WGetDownloader():

    def __init__(self, config, dataset):
        self.config = config
        self.dataset = dataset
        self.tier = 2

    @property
    def local_folder(self):
        return os.path.join(
            self.config['rootpath']['RAWOBS'][0],
            f'Tier{self.tier}',
            self.dataset
        )

    def download_folder(self, server_path, wget_options):
        # get filenames within the directory
        subprocess.check_output(
            ['wget'] + wget_options + [
                f'--directory-prefix={self.local_folder}',
                '--recursive',
                '--no-directories',
                '--no-clobber',
                f'{server_path}',
            ]
        )

    def download_file(self, server_path, wget_options):
        # get filenames within the directory
        subprocess.check_output(
            ['wget'] + wget_options + [
                f'--directory-prefix={self.local_folder}',
                '--no-directories',
                '--no-clobber',
                server_path,
            ]
        )


class NASADownloader(WGetDownloader):

    def __init__(self, config, dataset):
        super().__init__(config, dataset)
        self.tier = 3

        self._wget_common_options = [
            "--load-cookies=~/.urs_cookies",
            "--save-cookies=~/.urs_cookies",
            "--auth-no-challenge=on",
            "--keep-session-cookies",
        ]

    def download_folder(self, folder_path):
        wget_options = self._wget_common_options + [
            "-np",
            "--accept=nc,nc4"
        ]
        super().download_folder(folder_path, wget_options)

    def download_file(self, folder_path):
        super().download_file(folder_path, self._wget_common_options)
