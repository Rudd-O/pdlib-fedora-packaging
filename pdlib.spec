%global github_owner    goodspb
%global github_name     pdlib
%global github_commit   84436d5b9200e3388ca16851110d61b7c1439a8a
%global shortcommit     %(c=%{github_commit}; echo ${c:0:7})
%global debug_package   %{nil}

# needed to prevent mangling of the configure script by the macro percent configure
%define _lto_cflags     %{nil}

# my stuff for autobump
%define mybuildnumber %{?build_number}%{?!build_number:1}

Name:		pdlib
Version:	1.1.0
Release:	3.1.%{mybuildnumber}%{?dist}
Summary:	PHP extension to access the Dlib library
Group:		Development/Languages
License:	MIT
URL:		https://github.com/goodspb/pdlib
Source0:	https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{github_name}-%{version}.tar.gz

BuildRequires:	gcc-c++
BuildRequires:  sed
Buildrequires:  grep
BuildRequires:	php-devel
BuildRequires:	dlib-devel >= 19.8
BuildRequires:	pkgconfig(cblas)
BuildRequires:	pkgconfig(lapack)
BuildRequires:  strace
BuildRequires:  openblas-srpm-macros
BuildRequires:  openblas
BuildRequires:  lapack-devel
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}


%description
This extension provides a PHP implementation of the OpenCV library.
The extension offers two new functions. In principle, they differ
only by their return value. The first returns only the number of
faces found on the given image and the other an associative array
of their coordinates.


%prep
%setup -q -n %{name}-%{github_commit}

%{__cat} <<'EOF' > 40-pdlib.ini
extension=pdlib.so
EOF
sed -i 's/\r//' CREDITS

%build
set -x
phpize
# does not seem to be necessary
# percent configure already does this
cp -f configure configure.old
%configure
diff -Naur configure.old configure || true
make %{?_smp_mflags}

%install 
make install INSTALL_ROOT=$RPM_BUILD_ROOT INSTALL="install -p" 
install -p -D -m0644 40-pdlib.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d/40-pdlib.ini

%check
# Minimal load test of php extension
php --no-php-ini \
    --define extension_dir=${RPM_BUILD_ROOT}%{php_extdir} \
    --define extension=pdlib.so \
    --modules | grep pdlib

%files
%doc CREDITS
%license LICENSE
%config(noreplace) %{_sysconfdir}/php.d/40-pdlib.ini
%{php_extdir}/pdlib.so

%changelog
* Tue Apr 23 2024 Matias De lellis <mati86dl@gmail.com> 1.1.0-2
- Rebuild for dlib updates.

* Thu May 18 2023 Matias De lellis <mati86dl@gmail.com> 1.1.0-1
- Rebuild for dlib updates.

* Thu May 18 2023 Matias De lellis <mati86dl@gmail.com> 1.0.2-6
- Rebuild for dlib updates.

* Tue Aug 02 2022 Matias De lellis <mati86dl@gmail.com> 1.0.2-5
- Rebuild for dlib updates.

* Thu Nov 25 2021 Matias De lellis <mati86dl@gmail.com> 1.0.2-4
- Rebuild for fedora 35

* Tue May 18 2021 Matias De lellis <mati86dl@gmail.com> 1.0.2-3
- Explicitly requires cblas and lapack

* Tue May 18 2021 Matias De lellis <mati86dl@gmail.com> 1.0.2-2
- Rebuild to sync with the dlib package

* Sun Jul 26 2020 Matias De lellis <mati86dl@gmail.com> 1.0.2-1
- Update to last package

* Mon Nov 25 2019 Matias De lellis <mati86dl@gmail.com> - 1.0-2.20180830gitabb617b
- Rebuild with last dlib on copr.

* Mon Apr 15 2019 Matias De lellis <mati86dl@gmail.com> - 1.0-1.20180830gitabb617b
- Fix typo on loading extention file

* Thu Aug 30 2018 Matias De lellis <mati86dl@gmail.com> - 1.0-20180830gitabb617b
- Initial release

* Tue Aug 07 2018 Matias De lellis <mati86dl@gmail.com> - 0.1-20180720git091caba
- Initial package
