from leapp.workflows import Workflow
from leapp.workflows.phases import Phase
from leapp.workflows.flags import Flags
from leapp.workflows.tagfilters import TagFilter
from leapp.workflows.policies import Policies
from leapp.tags import IPUTag, FactsTag, ChecksTag, AttachPackageReposTag, PlanningTag, DownloadTag,\
    InterimPreparationTag, InitRamStartTag, NetworkTag, StorageTag, LateTestsTag, PreparationTag, RPMUpgradeTag, \
    ApplicationsTag, ThirdPartyApplicationsTag, FinalizationTag, FirstBootTag, ReportTag


class IPUWorkflow(Workflow):
    name = 'InplaceUpgrade'
    tag = IPUTag
    short_name = 'ipu'
    description = '''No description has been provided for the InplaceUpgrade workflow.'''

    class FactsCollectionPhase(Phase):
        name = 'Facts collection'
        filter = TagFilter(FactsTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class ChecksPhase(Phase):
        name = 'Checks'
        filter = TagFilter(ChecksTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class ReportsPhase(Phase):
        name = 'Reports'
        filter = TagFilter(ReportTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class AttachPackageReposPhase(Phase):
        name = 'AttachPackageRepos'
        filter = TagFilter(AttachPackageReposTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class PlanningPhase(Phase):
        name = 'Planning'
        filter = TagFilter(PlanningTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class DownloadPhase(Phase):
        name = 'Download'
        filter = TagFilter(DownloadTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class InterimPreparationPhase(Phase):
        name = 'InterimPreparation'
        filter = TagFilter(InterimPreparationTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags(restart_after_phase=True)

    class InitRamStartPhase(Phase):
        name = 'InitRamStart'
        filter = TagFilter(InitRamStartTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class NetworkPhase(Phase):
        name = 'Network'
        filter = TagFilter(NetworkTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class StoragePhase(Phase):
        name = 'Storage'
        filter = TagFilter(StorageTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class LateTestsPhase(Phase):
        name = 'LateTests'
        filter = TagFilter(LateTestsTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class PreparationPhase(Phase):
        name = 'Preparation'
        filter = TagFilter(PreparationTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class RPMUpgradePhase(Phase):
        name = 'RPMUpgrade'
        filter = TagFilter(RPMUpgradeTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class ApplicationsPhase(Phase):
        name = 'Applications'
        filter = TagFilter(ApplicationsTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class ThirdPartyApplicationsPhase(Phase):
        name = 'ThirdPartyApplications'
        filter = TagFilter(ThirdPartyApplicationsTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()

    class FinalizationPhase(Phase):
        name = 'Finalization'
        filter = TagFilter(FinalizationTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags(restart_after_phase=True)

    class FirstBootPhase(Phase):
        name = 'FirstBoot'
        filter = TagFilter(FirstBootTag)
        policies = Policies(Policies.Errors.FailPhase,
                            Policies.Retry.Phase)
        flags = Flags()
