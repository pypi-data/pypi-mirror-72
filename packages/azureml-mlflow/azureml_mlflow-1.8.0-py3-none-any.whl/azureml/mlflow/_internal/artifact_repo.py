# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowArtifactRepository** provides a class to up/download artifacts to storage backends in Azure."""

import logging
import os
import re

from functools import wraps

import mlflow
from mlflow.entities import FileInfo

from .utils import execute_func
from .store import AzureMLRestStore, AdbAzuremlRestStore, _VERSION_WARNING
from .utils import (get_service_context_from_artifact_url, artifact_uri_decomp,
                    get_aml_experiment_name, _EXP_NAME, _RUN_ID, _ARTIFACT_PATH)
from .run_artifacts_extension_client import RunArtifactsExtensionClient
from six.moves.urllib import parse

logger = logging.getLogger(__name__)

try:
    from mlflow.store.artifact.artifact_repo import ArtifactRepository
except ImportError:
    logger.warning(_VERSION_WARNING.format("ArtifactRepository from mlflow.store.artifact.artifact_repo"))
    from mlflow.store.artifact_repo import ArtifactRepository


class AzureMLflowArtifactRepository(ArtifactRepository):
    """Define how to upload (log) and download potentially large artifacts from different storage backends."""

    def __init__(self, artifact_uri):
        """
        Construct an AzureMLflowArtifactRepository object.

        This object is used with any of the functions called from mlflow or from
        the client which have to do with artifacts.

        :param artifact_uri: Azure URI. This URI is never used within the object,
            but is included here, as it is included in ArtifactRepository as well.
        :type artifact_uri: str
        """
        logger.debug("Initializing the AzureMLflowArtifactRepository")
        parsed_artifacts_url = parse.urlparse(artifact_uri)
        parsed_artifacts_path = artifact_uri_decomp(artifact_uri)
        experiment_name = parsed_artifacts_path[_EXP_NAME]
        logger.debug("AzureMLflowArtifactRepository for experiment {}".format(experiment_name))
        self._run_id = parsed_artifacts_path[_RUN_ID]
        logger.debug("AzureMLflowArtifactRepository for run id {}".format(self._run_id))
        self._path = parsed_artifacts_path.get(_ARTIFACT_PATH)
        logger.debug("AzureMLflowArtifactRepository for path {}".format(self._path))

        service_context = self._get_service_context(parsed_artifacts_url)
        self.run_artifacts = RunArtifactsExtensionClient(service_context, experiment_name)

    def _get_service_context(self, parsed_artifacts_url):
        from mlflow.tracking.client import MlflowClient
        try:
            store = MlflowClient()._tracking_client.store
        except:
            logger.warning(_VERSION_WARNING.format("MlflowClient()._tracking_client.store"))
            store = MlflowClient().store
        if isinstance(store, AzureMLRestStore):
            logger.debug("Using the service context from the {} store".format(store.__class__.__name__))
            return store.service_context
        elif isinstance(store, AdbAzuremlRestStore):
            return store.aml_store.service_context
        else:
            return get_service_context_from_artifact_url(parsed_artifacts_url)

    def _get_full_artifact_path(self, artifact_path=None):
        path_parts = []
        if self._path is None and artifact_path is None:
            return None
        if self._path:
            path_parts.append(self._path)
        if artifact_path:
            path_parts.append(artifact_path)
        return "/".join(path_parts)

    def log_artifact(self, local_file, artifact_path=None):
        """
        Log a local file as an artifact.

        Optionally takes an ``artifact_path``, which renames the file when it is
        uploaded to the ArtifactRepository.

        :param local_file: Absolute or relative path to the artifact locally.
        :type local_file: str
        :param artifact_path: Path to a file in the AzureML run's outputs, to where the artifact is uploaded.
        :type artifact_path: str
        """
        artifact_path = self._get_full_artifact_path(artifact_path)
        dest_path = self._normalize_slashes(self._build_dest_path(local_file, artifact_path))
        self.run_artifacts.upload_artifact(local_file, self._run_id, dest_path)

    def log_artifacts(self, local_dir, artifact_path=None):
        """
        Log the files in the specified local directory as artifacts.

        Optionally takes an ``artifact_path``, which specifies the directory of
        the AzureML run under which to place the artifacts in the local directory.

        :param local_dir: Directory of local artifacts to log.
        :type local_dir: str
        :param artifact_path: Directory within the run's artifact directory in which to log the artifacts.
        :type artifact_path: str
        """
        artifact_path = self._get_full_artifact_path(artifact_path)
        dest_path = self._normalize_slashes(self._build_dest_path(local_dir, artifact_path))
        local_dir = self._normalize_slash_end(local_dir)
        dest_path = self._normalize_slash_end(dest_path)

        if artifact_path is not None and artifact_path not in [".", "./"]:
            self.run_artifacts.upload_dir(local_dir,
                                          self._run_id,
                                          lambda fpath: dest_path + fpath[len(local_dir):])
        else:
            files = [os.path.join(local_dir, file_name) for file_name in os.listdir(local_dir)
                     if not os.path.isdir(os.path.join(local_dir, file_name))]
            dirs = [os.path.join(local_dir, dir_name) for dir_name in os.listdir(local_dir)
                    if os.path.isdir(os.path.join(local_dir, dir_name))]

            self.run_artifacts.upload_files(files, self._run_id, [os.path.basename(file_name) for file_name in files])
            for dir_name in dirs:
                self.run_artifacts.upload_dir(dir_name, self._run_id, skip_first_level=True)

    def list_artifacts(self, path):
        """
        Return all the artifacts for this run_uuid directly under path.

        If path is a file, returns an empty list. Will error if path is neither a
        file nor directory. Note that list_artifacts will not return valid
        artifact sizes from Azure.

        :param path: Relative source path that contain desired artifacts
        :type path: str
        :return: List of artifacts as FileInfo listed directly under path.
        """
        # get and filter by paths

        if path and self._path and not path.startswith(self._path):
            path = self._get_full_artifact_path(path)  # Adds prefix if called directly and it is not already set

        path_tokens = path.split("/") if path else []
        path_depth = len(path_tokens)
        artifacts = []
        for file_path in self.run_artifacts.get_file_paths(self._run_id):
            if path is None or file_path[:len(path)] == path and len(file_path) > len(path):
                artifacts.append(file_path)

        file_infos = []
        for artifact in artifacts:
            artifact_tokens = artifact.split("/")
            if len(artifact_tokens) == path_depth + 1:  # is a file
                file_infos.append(FileInfo(
                    path=artifact,
                    is_dir=False,
                    file_size=-1  # TODO: artifact size retrieval is not supported in Azure
                ))
            else:  # is a directory
                file_infos.append(FileInfo(
                    path="/".join(artifact_tokens[:path_depth + 1]),
                    is_dir=True,
                    file_size=-1  # TODO: artifact size retrieval is not supported in Azure
                ))

        return file_infos

    @wraps(ArtifactRepository.download_artifacts)
    def download_artifacts(self, artifact_path, dst_path=None):
        artifact_path = self._get_full_artifact_path(artifact_path)
        return super(AzureMLflowArtifactRepository, self).download_artifacts(artifact_path, dst_path=dst_path)

    def _download_file(self, remote_file_path, local_path, **kwargs):
        """
        Download the file at the specified relative remote path and save it at the specified local path.

        :param remote_file_path: Source path to the remote file, relative to the
        root directory of the artifact repository.
        :type remote_file_path: str
        :param local_path: The path to which to save the downloaded file.
        :type local_path: str
        """
        # kwargs handling was added to protect against a newly introduced kwarg causing a regression
        self.run_artifacts.download_artifact(self._run_id, remote_file_path, local_path)

    @staticmethod
    def _build_dest_path(local_path, artifact_path):
        return artifact_path if artifact_path else os.path.basename(local_path)

    @staticmethod
    def _normalize_slashes(path):
        return "/".join(path.split("\\"))

    @staticmethod
    def _normalize_slash_end(path):
        return path if path[-1] == "/" else path + "/"


class AdbAzuremlArtifactRepository(ArtifactRepository):
    def __init__(self, artifact_uri):
        self._artifact_uri = artifact_uri
        self.adb_artifact_repo = self.get_dbfs_artifact_repo(artifact_uri)
        self.amlflow_artifact_repo = self.get_aml_artifact_repo(artifact_uri)
        self.artifact_repos = self.get_artifact_repos()
        self.reader_repo = self.amlflow_artifact_repo

    def get_artifact_repos(self):
        return [self.adb_artifact_repo, self.amlflow_artifact_repo]

    def get_dbfs_artifact_repo(self, artifact_uri):
        try:
            from mlflow.store.artifact.dbfs_artifact_repo import DbfsRestArtifactRepository
        except ImportError:
            logger.warning(_VERSION_WARNING.format("DbfsRestArtifactRepository from " +
                                                   "mlflow.store.artifact.dbfs_artifact_repo"))
            from mlflow.store.dbfs_artifact_repo import DbfsRestArtifactRepository
        # dbfs artifact_uri has to have dbfs as prefix
        # by default it is dbfs:/databricks/mlflow/<exp_id>/<run_id>/artifacts
        artifact_uri = artifact_uri.replace("adbazureml", "dbfs", 1)
        logger.info("DBFS artifact uri is {}".format(artifact_uri))
        return DbfsRestArtifactRepository(artifact_uri)

    def get_aml_artifact_repo(self, artifact_uri):
        regex = "(.+)\\/(.+)\\/artifacts"
        mo = re.compile(regex).match(artifact_uri)
        if mo is None:
            logger.debug("The given artifact uri {} does not match regex {}".format(artifact_uri, regex))
            raise ValueError("Invalid artifact_uri format {}".format(artifact_uri))
        run_id = mo.group(2)
        logger.info("Extracting run_id {} from artifact uri {}".format(run_id, artifact_uri))
        client = mlflow.tracking.MlflowClient()
        run = client.get_run(run_id)
        experiment_id = run.info.experiment_id
        experiment_name = client.get_experiment(experiment_id)._name
        logger.info("Mlflow Run with run_id {} has experiment id {} and experiment name {}".format(run_id,
                                                                                                   experiment_id,
                                                                                                   experiment_name))
        experiment_name = get_aml_experiment_name(experiment_name)
        aml_artifact_uri = "azureml://experiments/{}/runs/{}/artifacts".format(experiment_name, run_id)
        logger.info("AML artifact uri is {}".format(aml_artifact_uri))
        return AzureMLflowArtifactRepository(aml_artifact_uri)

    def log_artifact(self, *args, **kwargs):
        operation = "log_artifact"
        execute_func(lambda repo, *args, **kwargs: repo.log_artifact(*args, **kwargs),
                     self.artifact_repos, operation, *args, **kwargs)

    def log_artifacts(self, *args, **kwargs):
        operation = "log_artifacts"
        execute_func(lambda repo, *args, **kwargs: repo.log_artifacts(*args, **kwargs),
                     self.artifact_repos, operation, *args, **kwargs)

    def list_artifacts(self, path):
        return self.adb_artifact_repo.list_artifacts(path)

    def _download_file(self, *args, **kwargs):
        return self.reader_repo._download_file(*args, **kwargs)
