from boto3.s3.transfer import TransferConfig
from pathlib import Path
from typing import Union

import boto3
import botocore
import threading


class S3(object):
    """ S3 client, boto3.s3 wrapper
    """

    client_config = botocore.config.Config(max_pool_connections=512,)
    config = TransferConfig(
        multipart_threshold=1024 * 64,
        max_concurrency=1024,
        multipart_chunksize=1024 * 64,
        use_threads=True,
    )

    def __init__(self, company="", project_id="", creds=None):
        if not company:
            raise ValueError("Please provide a company_id")
        if not project_id:
            raise ValueError("Please provide a project_id")
        if not creds:
            raise ValueError("Please provide a credentials for s3 access")
        if not creds.get("AccessKeyId"):
            raise ValueError("Please provide a AccessKeyId for s3 access")
        if not creds.get("SecretAccessKey"):
            raise ValueError("Please provide a SecretAccessKey for s3 access")
        if not creds.get("SessionToken"):
            raise ValueError("Please provide a SessionToken for s3 access")
        self._client = boto3.client(
            "s3",
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"],
            config=self.client_config,
        )
        self._company = company
        self._project_id = project_id
        self._bucket = "immuno-prism"

    def upload_files(self, files: list):
        if isinstance(files, (str, Path)):
            files = [files]
        elif isinstance(files, list):
            pass
        else:
            raise ValueError(
                f"Cannot upload non str or non Path or non list type: {type(files)}"
            )
        for i, file in enumerate(files):
            if isinstance(file, Path):
                file = file.as_posix()
            file_size = Path(file).stat().st_size
            destination_name = (
                Path(self._company) / self._project_id / "uploads" / Path(file).name
            )
            self._client.upload_file(
                file,
                self._bucket,
                destination_name.as_posix(),
                Config=S3.config,
                Callback=ProgressPercentage(i + 1, file, len(files), file_size),
            )
            print(f"Upload complete: {Path(file).name:<46}")
        print(f"Uploads {len(files)} of {len(files)} complete.")
        return True

    def remove_file(self, file_name):
        destination_name = (
            Path(self._company) / self._project_id / "uploads" / file_name
        )
        if self._client.list_objects_v2(
            Bucket="immuno-prism", Prefix=destination_name.as_posix()
        ).get("Contents"):
            self._client.delete_object(
                Bucket="immuno-prism", Key=destination_name.as_posix()
            )
            print(f"Deleted {file_name}")
            return True
        print(f"File {file_name} not found.")
        return False

    def remove_files(self):
        destination_name = Path(self._company) / self._project_id
        files = self._client.list_objects_v2(
            Bucket="immuno-prism", Prefix=destination_name.as_posix()
        ).get("Contents", {})
        for file in files:
            print(file)


class ProgressPercentage(object):
    """ Callback that calculates the current percent downloaded for given file.
    """

    def __init__(self, index: int, file_name: str, total: int, file_size: int):
        self._file_name = file_name
        if not Path(self._file_name).exists():
            raise ValueError(f"File not found: {file_name}")
        self._seen_so_far = 0
        self._lock = threading.Lock()
        self.index = index
        self.total = total
        self.file_size = file_size

    def __call__(self, bytes_amount: int):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self.file_size) * 100
            formatted_perc = f"{percentage:.2f}"
            print(
                f"\033[1m{Path(self._file_name).name:<50}\033[0m {self.index:<4} of {self.total:<4} progress: \033[1m({formatted_perc:>6}%)\033[0m   \033[92m{self.progress_bar(percentage)}\033[0m {int(self.file_size*percentage//100000000)}/{self.file_size//1000000}MB",
                end="\r",
            )

    @staticmethod
    def progress_bar(percent: Union[float, int]) -> str:
        position = int(percent // 2)
        blank = 50 - position
        return f"{'|'*position+' '*blank}"
