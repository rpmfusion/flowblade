#For git snapshots, set to 0 to use release instead:
%global usesnapshot 0
%if 0%{?usesnapshot}
%global commit0 21710f51e7f14e14bfed998ef2df8cc444d26776
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global snapshottag .git%{shortcommit0}
%endif
%global unique_name io.github.jliljebl.Flowblade

Name:           flowblade
%if 0%{?usesnapshot}
Version:        2.0
Release:        4.git%{?snapshottag}%{?dist}
%else
Version:        2.0
Release:        4%{?dist}
%endif
License:        GPLv3
Summary:        Multitrack non-linear video editor for Linux
Url:            https://github.com/jliljebl/flowblade
%if 0%{?usesnapshot}
Source0:        %{url}/archive/%{commit0}/%{name}-%{version}-%{shortcommit0}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif
Patch0:         flowblade_sys_path.patch

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires:       ffmpeg
Requires:       python2-mlt
Requires:       frei0r-plugins >= 1.4
Requires:       gmic
Requires:       gtk3
# This dependency isn't available anymore since f30
%if 0%{?fedora} && 0%{?fedora} < 30
Requires:       ladspa-swh-plugins
%endif
Requires:       ladspa-calf-plugins
Requires:       librsvg2
Requires:       python2-numpy
Requires:       python2-pillow
%if 0%{?fedora} >= 28
Requires:       python2-dbus
Requires:       python2-gobject
%else
Requires:       python-dbus
Requires:       python-gobject
%endif
Requires:       mlt-freeworld
Requires:       shared-mime-info%{?_isa}

BuildArch:      noarch

%description
Flowblade Movie Editor is a multitrack non-linear video editor for Linux
released under GPL 3 license.

Flowblade is designed to provide a fast, precise and robust editing 
experience.

In Flowblade clips are usually automatically placed tightly after or 
between clips when they are inserted on the timeline. Edits are fine 
tuned by trimming in and out points of clips, or by cutting and deleting 
parts of clips.

Flowblade provides powerful tools to mix and filter video and audio. 

%prep
%if 0%{?usesnapshot}
%setup -qn %{name}-%{commit0}
%else
%setup -q -n %{name}-%{version}
%endif

# fix to  /usr/bin/flowblade
%patch0 -p1

# fix wrong-script-interpreter errors
sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/python2|g' flowblade-trunk/Flowblade/launch/*
sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/python2|g' flowblade-trunk/Flowblade/tools/clapperless.py

# fix to %%{_datadir}/locale
sed -i "s|respaths.LOCALE_PATH|'%{_datadir}/locale'|g" flowblade-trunk/Flowblade/translations.py


%build 
cd flowblade-trunk
%py2_build

%install 
cd flowblade-trunk
%py2_install 

# fix permissions
chmod +x %{buildroot}%{python2_sitelib}/Flowblade/launch/*

# setup of mime is already done, so for what we need this file ?
rm %{buildroot}/usr/lib/mime/packages/flowblade

# move .mo files to /usr/share/locale the right place
for i in $(ls -d %{buildroot}%{python2_sitelib}/Flowblade/locale/*/LC_MESSAGES/ | sed 's/\(^.*locale\/\)\(.*\)\(\/LC_MESSAGES\/$\)/\2/') ; do
    mkdir -p %{buildroot}%{_datadir}/locale/$i/LC_MESSAGES/
    mv %{buildroot}%{python2_sitelib}/Flowblade/locale/$i/LC_MESSAGES/%{name}.mo \
        %{buildroot}%{_datadir}/locale/$i/LC_MESSAGES/
done

# E: non-executable-script
chmod a+x %{buildroot}%{python2_sitelib}/Flowblade/tools/clapperless.py

install -d -m 0755 %{buildroot}%{python2_sitelib}/Flowblade/res/css
cp Flowblade/res/css/gtk-flowblade-dark.css %{buildroot}%{python2_sitelib}/Flowblade/res/css

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{unique_name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.appdata.xml

%files -f flowblade-trunk/%{name}.lang
%doc flowblade-trunk/README
%license flowblade-trunk/COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{unique_name}.desktop
%{_mandir}/man1/%{name}.1.*
%{_datadir}/mime/packages/%{unique_name}.xml
%{_datadir}/appdata/%{unique_name}.appdata.xml
%{_datadir}/icons/hicolor/128x128/apps/%{unique_name}.png
%{python2_sitelib}/Flowblade/
%{python2_sitelib}/%{name}*

%changelog
* Mon Apr 08 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.0-4
- Drop ladspa-swh-plugins on f30+

* Fri Mar 08 2019 Sérgio Basto <sergio@serjux.com> - 2.0-3
- Requires python2-mlt instead mlt-python

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Feb 04 2019 Martin Gansser <martinkg@fedoraproject.org> - 2.0-1
- Update to 2.0-1

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.16.0-5.git4c25c3c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 14 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.16.0-4.git4c25c3c
- Update to 1.16.0-4.git4c25c3c

* Thu Jun 28 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.16.0-3.git3fdb76d
- Update to 1.16.0-3.git3fdb76d
- Add BR libappstream-glib

* Sun Apr 01 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.16.0-2.gitd2f153f
- Use url macro to shorten line
- Fix python requires for f28 and remove old mlt-freeworld conditional
- Fix directory ownership
- Remove scriplets

* Sun Apr 01 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.16.0-1.gitd2f153f
- Update to 1.16.0-1.gitd2f153f

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.14.0-2.gitc2cc6a8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 06 2017 Martin Gansser <martinkg@fedoraproject.org> - 1.14.0-1.gitc2cc6a8
- Update to 1.14.0-1.gitc2cc6a8

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.12.0-2.gitfd577a9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 24 2017 Martin Gansser <martinkg@fedoraproject.org> - 1.12.0-1.gitfd577a9
- Update to 1.12.0-1.gitfd577a9

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.10.0-4.git9365491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.10.0-3.git25c07ce
- rebuild

* Fri Dec 16 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.10.0-2.git25c07ce
- Readd ffmpeg
- Add Requires mlt-freeworld in a if clause

* Thu Dec 15 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.10.0-1.git25c07ce
- Update to 1.10.0-1.git25c07ce
- Dropped Requires ffmpeg
- Add Requires mlt-freeworld

* Thu Sep 22 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.8.0-1.git9365491
- Update to 1.8.0-1.git9365491

* Fri Aug 26 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-5.gitc847b32
- Fix python requires for F23 (rfbz#4213)

* Wed Aug 17 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-4.gitc847b32
- Update package requires for git snapshot

* Mon Aug 01 2016 Sérgio Basto <sergio@serjux.com> - 1.6.0-3.gitc847b32
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 30 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.6.0-2.gitc847b32
- Update to 1.6.0-2.gitc847b32

* Thu Jun 09 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.6.0-1.git50f6fca
- Update to 1.6.0

* Mon Nov 30 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.4.0-1.git3f5d08d
- Update to 1.4.0

* Fri Sep 11 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.2.0-1.git7d98158
- Update to 1.2.0

* Thu Aug 27 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-6.git7d98158
- spec cleanup

* Sat Jul 18 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-5.git94f69ce
- dropped gnome-python2-gnomevfs requirement
- dropped ladspa requirement
- dropped pycairo requirement
- dropped mlt requirement
- dropped calf requirement
- dropped numpy requirement
- dropped cairo requirement

* Mon Jun 22 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-4.git94f69ce
- Fix file permissions before and after build
- Remove flowblade mime file 
- move .mo files to /usr/share/locale

* Sun Jun 21 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-3.git94f69ce
- added flowblade.patch
- put setup.py into %%build section
- added macro %%find_lang
- fixed locale path 

* Sat Jun 20 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-2.git94f69ce
- used macro %%{python_sitearch}
- spec file cleanup
- mime file belong to %%{_libexecdir}

* Fri Jun 19 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-1.git94f69ce
- Update to 1.1.0

* Fri Mar 20 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.18.0-1
- Updated to 0.18.0

* Sat Jul 05 2014 David Vásquez <davidjeremias82@ dat com> 0.12.0-1
- Updated to 0.12.0

* Thu Oct 24 2013 David Vásquez <davidjeremias82@ dat com> 0.10.0-1
- Initial build rpm Fedora

