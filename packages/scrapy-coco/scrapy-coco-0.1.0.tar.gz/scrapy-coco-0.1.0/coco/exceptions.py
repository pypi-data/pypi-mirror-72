# MANIFEST
class ManifestValidationError(Exception):
    pass


class ManifestLoadError(Exception):
    pass


# STAGE
class SuppressStage(Exception):
    pass


class SuppressStagesException(Exception):
    pass


# PAGINATION
class NextPageNotFoundError(Exception):
    pass


class PaginationPageThresholdReached(Exception):
    pass
