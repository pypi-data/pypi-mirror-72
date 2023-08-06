from poetry.core.packages import Package
from poetry.utils._compat import Path
from poetry.utils._compat import metadata
from poetry.utils.env import Env

from .repository import Repository


_VENDORS = Path(__file__).parent.parent.joinpath("_vendor")


class InstalledRepository(Repository):
    @classmethod
    def load(cls, env):  # type: (Env) -> InstalledRepository
        """
        Load installed packages.
        """
        repo = cls()
        seen = set()

        for entry in reversed(env.sys_path):
            for distribution in sorted(
                metadata.distributions(path=[entry]), key=lambda d: str(d._path),
            ):
                name = distribution.metadata["name"]
                path = Path(str(distribution._path))
                version = distribution.metadata["version"]
                package = Package(name, version, version)
                package.description = distribution.metadata.get("summary", "")

                if package.name in seen:
                    continue

                try:
                    path.relative_to(_VENDORS)
                except ValueError:
                    pass
                else:
                    continue

                seen.add(package.name)

                repo.add_package(package)

                is_standard_package = True
                try:
                    path.relative_to(env.site_packages)
                except ValueError:
                    is_standard_package = False

                if is_standard_package:
                    if (
                        path.name.endswith(".dist-info")
                        and env.site_packages.joinpath(
                            "{}.pth".format(package.pretty_name)
                        ).exists()
                    ):
                        with env.site_packages.joinpath(
                            "{}.pth".format(package.pretty_name)
                        ).open() as f:
                            directory = Path(f.readline().strip())
                            package.source_type = "directory"
                            package.source_url = directory.as_posix()

                    continue

                src_path = env.path / "src"

                # A VCS dependency should have been installed
                # in the src directory. If not, it's a path dependency
                try:
                    path.relative_to(src_path)

                    from poetry.core.vcs.git import Git

                    git = Git()
                    revision = git.rev_parse("HEAD", src_path / package.name).strip()
                    url = git.remote_url(src_path / package.name)

                    package.source_type = "git"
                    package.source_url = url
                    package.source_reference = revision
                except ValueError:
                    package.source_type = "directory"
                    package.source_url = str(path.parent)

        return repo
