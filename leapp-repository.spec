%global debug_package %{nil}
%global gittag master
%global dist %{nil}

%global repositorydir %{_datadir}/leapp-repository/repositories
%global custom_repositorydir %{_datadir}/leapp-repository/custom-repositories

Name:       leapp-repository
Version:    0.3
Release:    1%{?dist}
Summary:    Repositories for leapp

License:    ASL 2.0
URL:        https://leapp-to.github.io
Source0:    https://github.com/leapp-to/leapp-actors/archive/%{gittag}/leapp-actors-%{version}.tar.gz
BuildArch:  noarch
Requires:   dnf >= 2.7.5
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:   systemd-container
%endif

Requires:   augeas
%if 0%{?rhel} && 0%{?rhel} == 7
Requires:   python-augeas
%else
Requires:   python3-augeas
%endif

%description
Repositories for leapp

%prep
%autosetup -n leapp-actors-%{gittag}


%build
make build

%install
install -m 0755 -d %{buildroot}%{custom_repositorydir}
install -m 0755 -d %{buildroot}%{repositorydir}
cp -r repos/* %{buildroot}%{repositorydir}/

install -m 0755 -d %{buildroot}%{_sysconfdir}/leapp/repos.d/
for DIRECTORY in $(find  repos/  -mindepth 1 -maxdepth 1 -type d);
do
    REPOSITORY=$(basename $DIRECTORY)
    echo "Enabling repository $REPOSITORY"
    ln -s  %{repositorydir}/$REPOSITORY  %{buildroot}%{_sysconfdir}/leapp/repos.d/$REPOSITORY
done;


%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_sysconfdir}/leapp/repos.d/*
%{repositorydir}/*
%dir %{custom_repositorydir}


%changelog
* Mon Apr 16 2018 Vinzenz Feenstra <evilissimo@redhat.com> - 0.3-1
- Initial RPM
