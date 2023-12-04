%{?python_enable_dependency_generator}
# https://pagure.io/koji/issue/659
%global debug_package %{nil}

Summary:	RPM macros for building Rust packages on various architectures
Name:		rust-packaging
Version:	25.2
Release:	1
Group:		System/Packaging
License:	MIT
URL:		https://pagure.io/fedora-rust/rust-packaging
Source:		https://pagure.io/fedora-rust/rust-packaging/archive/%{version}/rust-packaging-%{version}.tar.gz
Patch0:		macros.cargo-dont-barf-on-missing-repo-files.patch
ExclusiveArch:	%{rust_arches}

# gawk is needed for stripping dev-deps in macro
Requires:	gawk
Requires:	python-cargo2rpm
Requires:	python-rust2rpm
Requires:	rust-srpm-macros
Requires:	rust
Requires:	cargo

# Try to remain compatible with Fedora packages
Provides:	cargo-rpm-macros = %{EVRD}

%description
The package provides macros for building projects in Rust
on various architectures.

%package -n rust-srpm-macros
Summary:	RPM macros for building Rust source packages
Group:		System/Packaging

%description -n rust-srpm-macros
RPM macros for building Rust source packages.

%prep
%autosetup -p1
sed -i -e 's/i686/%%{ix86}/' macros.d/macros.rust-srpm
sed -i -e 's/x86_64/%%{x86_64}/' macros.d/macros.rust-srpm
sed -i -e 's/armv7hl/armv7hnl/' macros.d/macros.rust-srpm

%build

%install
install -D -p -m 0644 -t %{buildroot}%{_rpmmacrodir} macros.d/macros.rust macros.d/macros.cargo macros.d/macros.rust-srpm
install -D -p -m 0644 -t %{buildroot}%{_fileattrsdir} fileattrs/cargo.attr

%files
%license LICENSE
%{_rpmmacrodir}/macros.rust
%{_rpmmacrodir}/macros.cargo
%{_fileattrsdir}/cargo.attr

%files -n rust-srpm-macros
%{_rpmmacrodir}/macros.rust-srpm
