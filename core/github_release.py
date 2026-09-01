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

    def get_release_by_tag(
        self,
        tag
    ):

        url = (
            f"{self.api_url}/releases/tags/"
            f"{tag}"
        )

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return response.json()

    def create_release(
        self,
        tag,
        name,
        description=""
    ):

        existing = self.get_release_by_tag(
            tag
        )

        if existing:

            print(
                "GitHub Release уже существует:",
                tag
            )

            return existing

        url = f"{self.api_url}/releases"

        data = {
            "tag_name": tag,
            "name": name,
            "body": description,
            "draft": False,
            "prerelease": False
        }

        print("GITHUB RELEASE DATA:")
        print(data)

        response = requests.post(
            url,
            headers=self.headers,
            json=data,
            timeout=30
        )

        if response.status_code >= 400:

            print("GITHUB ERROR:")
            print(response.text)

        response.raise_for_status()

        return response.json()

    def get_assets(
        self,
        release
    ):

        url = release.get(
            "assets_url",
            ""
        )

        if not url:

            raise Exception(
                "GitHub не вернул assets_url"
            )

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def delete_asset(
        self,
        asset
    ):

        asset_id = asset.get(
            "id"
        )

        if not asset_id:

            raise Exception(
                "GitHub не вернул ID asset"
            )

        url = (
            f"{self.api_url}/"
            f"releases/assets/"
            f"{asset_id}"
        )

        response = requests.delete(
            url,
            headers=self.headers,
            timeout=30
        )

        if response.status_code != 204:

            print(
                "GITHUB DELETE ASSET ERROR:"
            )

            print(
                response.text
            )

        response.raise_for_status()

        print(
            "GitHub asset удалён:",
            asset.get("name")
        )

        return True

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
            "Content-Type":
            "application/octet-stream"
        }

        file_size = os.path.getsize(
            file_path
        )

        print(
            "Загрузка IPA в GitHub Release:"
        )

        print(
            "  file:",
            file_path
        )

        print(
            "  name:",
            file_name
        )

        print(
            "  size:",
            file_size
        )

        with open(
            file_path,
            "rb"
        ) as file:

            response = requests.post(
                url,
                headers=headers,
                data=file,
                timeout=1800
            )

        if response.status_code >= 400:

            print(
                "GITHUB UPLOAD ERROR:"
            )

            print(
                response.text
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
