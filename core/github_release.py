import os
import requests


class GitHubRelease:

    def __init__(
        self,
        owner,
        repo,
        token
    ):

        self.owner = owner
        self.repo = repo
        self.token = token

        self.api_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}"
        )

        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def create_release(
        self,
        tag,
        name,
        description=""
    ):

        url = f"{self.api_url}/releases"

        data = {
            "tag_name": tag,
            "name": name,
            "body": description,
            "draft": False,
            "prerelease": False
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=data,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def upload_file(
        self,
        release,
        file_path
    ):

        upload_url = release.get(
            "upload_url",
            ""
        )

        if not upload_url:
            raise Exception(
                "GitHub не вернул upload_url"
            )

        upload_url = upload_url.split(
            "{",
            1
        )[0]

        file_name = os.path.basename(
            file_path
        )

        url = (
            f"{upload_url}"
            f"?name={file_name}"
        )

        headers = {
            **self.headers,
            "Content-Type": "application/octet-stream"
        }

        with open(
            file_path,
            "rb"
        ) as file:

            response = requests.post(
                url,
                headers=headers,
                data=file,
                timeout=600
            )

        response.raise_for_status()

        return response.json()

    def get_download_url(
        self,
        asset
    ):

        url = asset.get(
            "browser_download_url",
            ""
        )

        if not url:
            raise Exception(
                "GitHub не вернул URL файла"
            )

        return url
