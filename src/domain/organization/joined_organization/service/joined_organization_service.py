from domain.organization.joined_organization.repository import JoinedOrganizationRepository

class JoinedOrganizationService:

    def __init__(self, joined_organization_repository: JoinedOrganizationRepository):
        self.joined_organization_repository = joined_organization_repository
