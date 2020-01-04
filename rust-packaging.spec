%bcond_without check
%{?python_enable_dependency_generator}
# https://pagure.io/koji/issue/659
%global debug_package %{nil}

Name:           rust-packaging
Version:        10
Release:        %mkrel 2
Summary:        RPM macros for building Rust packages on various architectures
%if 0%{?mageia}
Group:          System/Packaging
%endif
License:        MIT
URL:            https://pagure.io/fedora-rust/rust2rpm
Source:         https://releases.pagure.org/fedora-rust/rust2rpm/rust2rpm-%{version}.tar.xz
# TODO: See if we can manage to keep using inplace feature
Patch0001:      0001-macros-Do-not-use-awk-s-inplace-feature.patch

ExclusiveArch:  %{rust_arches}

# gawk is needed for stripping dev-deps in macro
Requires:       gawk
Requires:       python3-rust2rpm = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       rust-srpm-macros = %{version}
Requires:       rust
Requires:       cargo

%description
The package provides macros for building projects in Rust
on various architectures.

%package     -n python3-rust2rpm
Summary:        Convert Rust packages to RPM
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with check}
BuildRequires:  python3-pytest
BuildRequires:  cargo
BuildRequires:  python3dist(semantic-version)
%endif
Requires:       cargo
Provides:       rust2rpm = %{version}-%{release}
%{?python_provide:%python_provide python3-rust2rpm}

%description -n python3-rust2rpm
%{summary}.

%prep
%autosetup -n rust2rpm-%{version} -p1

%build
%py3_build

%install
%py3_install
install -D -p -m 0644 -t %{buildroot}%{_rpmmacrodir} data/macros.rust data/macros.cargo
install -D -p -m 0644 -t %{buildroot}%{_fileattrsdir} data/cargo.attr

%if %{with check}
%check
py.test-%{python3_version} -vv test.py
%endif

%files
%license LICENSE
%{_rpmmacrodir}/macros.rust
%{_rpmmacrodir}/macros.cargo
%{_fileattrsdir}/cargo.attr

%files -n python3-rust2rpm
%license LICENSE
%{_bindir}/rust2rpm
%{_bindir}/cargo-inspector
%{python3_sitelib}/rust2rpm-*.egg-info/
%{python3_sitelib}/rust2rpm/
