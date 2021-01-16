%{?python_enable_dependency_generator}
# https://pagure.io/koji/issue/659
%global debug_package %{nil}

Name:           rust-packaging
Version:        17
Release:        1
Summary:        RPM macros for building Rust packages on various architectures
Group:          System/Packaging
License:        MIT
URL:            https://pagure.io/fedora-rust/rust2rpm
Source:         https://pagure.io/fedora-rust/rust2rpm/archive/v%{version}/rust2rpm-v%{version}.tar.gz

# gawk is needed for stripping dev-deps in macro
Requires:       gawk
Requires:       python-rust2rpm 
Requires:       rust-srpm-macros
Requires:       rust
Requires:       cargo

%description
The package provides macros for building projects in Rust
on various architectures.

%package -n python-rust2rpm
Summary:        Convert Rust packages to RPM
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  cargo

Requires:       cargo
Provides:       rust2rpm = %{version}-%{release}
%{?python_provide:%python_provide python-rust2rpm}

%description -n python-rust2rpm
%{summary}.

%prep
%autosetup -n rust2rpm-v%{version} -p1

%build
%py_build

%install
%py_install
install -D -p -m 0644 -t %{buildroot}%{_rpmmacrodir} data/macros.rust data/macros.cargo
install -D -p -m 0644 -t %{buildroot}%{_fileattrsdir} data/cargo.attr

%files
%license LICENSE
%{_rpmmacrodir}/macros.rust
%{_rpmmacrodir}/macros.cargo
%{_fileattrsdir}/cargo.attr

%files -n python-rust2rpm
%license LICENSE
%{_bindir}/rust2rpm
%{_bindir}/cargo-inspector
%{python_sitelib}/rust2rpm-*.egg-info/
%{python_sitelib}/rust2rpm/
