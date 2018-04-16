%global debug_package %{nil}
%global gittag master
%global dist %{nil}

%global repositorydir %{_datadir}/leapp-repository/repositories

Name:       leapp-repository
Version:    0.3
Release:    1%{?dist}
Summary:    Repositories for leapp

License:    ASL 2.0
URL:        https://leapp-to.github.io
Source0:    https://github.com/leapp-to/leapp-actors/archive/%{gittag}/leapp-actors-%{version}.tar.gz
BuildArch:  noarch
%description
Repositories for leapp

%prep
%autosetup -n leapp-actors-%{gittag}


%build
make build

%install
install -m 0775 -d %{buildroot}%{repositorydir}
cp -r repos/* %{buildroot}%{repositorydir}/

install -m 0775 -d %{buildroot}%{_sysconfdir}/leapp/repos.d/
ln -s  %{repositorydir}/common  %{buildroot}%{_sysconfdir}/leapp/repos.d/common
ln -s  %{repositorydir}/upgrade  %{buildroot}%{_sysconfdir}/leapp/repos.d/upgrade


%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_sysconfdir}/leapp/repos.d/upgrade
%{_sysconfdir}/leapp/repos.d/common
%{repositorydir}/*


%changelog
* Mon Apr 16 2018 Vinzenz Feenstra <evilissimo@redhat.com> - 0.3-1
- Initial RPM
