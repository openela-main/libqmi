%if 0%{?fedora} || 0%{?rhel} >= 9
%bcond_without qrtr
%else
%bcond_with qrtr
%endif

Name: libqmi
Version: 1.32.2
Release: 3%{?dist}
Summary: Support library to use the Qualcomm MSM Interface (QMI) protocol
License: LGPLv2+
URL: http://freedesktop.org/software/libqmi
Source: https://gitlab.freedesktop.org/mobile-broadband/libqmi/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0: 0001-Disable-docs-check.patch

BuildRequires: meson >= 0.53
BuildRequires: gcc
BuildRequires: glib2-devel >= 2.56
BuildRequires: gobject-introspection-devel
BuildRequires: gtk-doc
BuildRequires: pkgconfig(gudev-1.0) >= 147
BuildRequires: libmbim-devel >= 1.18.0
%if %{with qrtr}
BuildRequires: libqrtr-glib-devel
%endif
BuildRequires: python3
BuildRequires: help2man

%description
This package contains the libraries that make it easier to use QMI functionality
from applications that use glib.


%package devel
Summary: Header files for adding QMI support to applications that use glib
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel%{?_isa}
Requires: pkgconfig

%description devel
This package contains the header and pkg-config files for development
applications using QMI functionality from applications that use glib.


%package utils
Summary: Utilities to use the QMI protocol from the command line
Requires: %{name}%{?_isa} = %{version}-%{release}
License: GPLv2+

%description utils
This package contains the utilities that make it easier to use QMI functionality
from the command line.


%prep
%autosetup -p1


%build
# Let's avoid BuildRequiring bash-completion because it changes behavior
# of shell, at least until the .pc file gets into the -devel subpackage.
# We'll just install the bash-completion file ourselves.
%meson -Dgtk_doc=true -Dbash_completion=false \
%if %{with qrtr}
	-Dqrtr=true
%else
	-Dqrtr=false
%endif
%meson_build
%ninja_build -C %{_vpath_builddir} libqmi-glib-doc


%install
%meson_install
find %{buildroot}%{_datadir}/gtk-doc |xargs touch --reference meson.build
find %{buildroot} -type f -name "*.la" -delete
mkdir -p %{buildroot}%{_datadir}/bash-completion
cp -a src/qmicli/qmicli %{buildroot}%{_datadir}/bash-completion


%check
%meson_test


%ldconfig_scriptlets


%files
%license COPYING.LIB
%doc NEWS AUTHORS README.md
%{_libdir}/libqmi-glib.so.*
%{_libdir}/girepository-1.0/Qmi-1.0.typelib


%files devel
%{_includedir}/libqmi-glib/
%{_libdir}/pkgconfig/qmi-glib.pc
%{_libdir}/libqmi-glib.so
%{_datadir}/gtk-doc/html/libqmi-glib/
%{_datadir}/gir-1.0/Qmi-1.0.gir


%files utils
%license COPYING
%{_bindir}/qmicli
%{_bindir}/qmi-network
%{_bindir}/qmi-firmware-update
%{_datadir}/bash-completion
%{_libexecdir}/qmi-proxy
%{_mandir}/man1/*


%changelog
* Mon Dec 12 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.32.2-3
- Update to 1.32.2
- Build without QRTR

* Fri Oct 1 2021 Ana Cabral <acabral@redhat.com> - 1.30.2-1
- Upgrade to 1.30.2

* Mon Jul 19 2021 Thomas Haller <thaller@redhat.com> - 1.24.0-3
- fix crash in qmi_endpoint_is_open() (rh #1976888)

* Mon Jul 19 2021 Thomas Haller <thaller@redhat.com> - 1.24.0-2
- fix crash and detect QMI port over smdpkt subsystem (rh #1976886)

* Wed Oct 16 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.24.0-1
- Update to 1.24.0

* Mon May 06 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.22.4-1
- Update to 1.22.4

* Fri Jun 29 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.20.0-4
- Change to Python 3 as a build dependency

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.20.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Lubomir Rintel <lkundrak@v3.sk> - 1.20.0-1
- Update to 1.18.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.18.0-1
- Update to 1.18.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 15 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.16.2-1
- Update to 1.16.2

* Tue Oct 04 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.16.0-2
- Enable hardening

* Fri Jul 08 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.16.0-1
- Update to 1.16.0

* Tue May 03 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.14.2-1
- Update to 1.14.2

* Mon Mar 21 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.14.0-1
- Update to 1.14.0 release

* Tue Mar 01 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 1.12.6-3
- Fix FTBFS with GCC 6 (#1307733)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 18 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.12.6-1
- Update to 1.12.6 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.12.4-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 11 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.12.4-1
- Update to 1.12.4 release

* Tue Feb 10 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.12.2-1
- Clean up the spec file a bit
- Update to 1.12.2 release

* Thu Jan 15 2015 Dan Williams <dcbw@redhat.com> - 1.12.0-1
- Update to 1.12.0 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug  5 2014 Dan Williams <dcbw@redhat.com> - 1.10.2
- Update to 1.10.2 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb  1 2014 poma <poma@gmail.com> - 1.8.0-1
- Update to 1.8.0 release

* Fri Sep  6 2013 Dan Williams <dcbw@redhat.com> - 1.6.0-1
- Update to 1.6.0 release

* Fri Jun  7 2013 Dan Williams <dcbw@redhat.com> - 1.4.0-1
- Update to 1.4.0 release

* Fri May 10 2013 Dan Williams <dcbw@redhat.com> - 1.3.0-1.git20130510
- Initial Fedora release

