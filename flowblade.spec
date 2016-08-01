#https://github.com/jliljebl/flowblade/commit/c847b323037eed2099e770f916f3ec3f9354ac9c
%global commit0  c847b323037eed2099e770f916f3ec3f9354ac9c
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           flowblade
Version:        1.6.0
Release:        3.git%{shortcommit0}%{?dist}
License:        GPLv3
Summary:        Multitrack non-linear video editor for Linux
Url:            https://github.com/jliljebl/flowblade
Source0:        https://github.com/jliljebl/flowblade/archive/%{commit0}/%{name}-%{version}-%{shortcommit0}.tar.gz
Patch0:         flowblade-001_sys_path.patch

BuildRequires:  desktop-file-utils
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  librsvg2-devel

Requires:       ffmpeg 
Requires:       pygtk2 
Requires:       ladspa-swh-plugins
Requires:       ladspa-calf-plugins
Requires:       sox 
Requires:       frei0r-plugins >= 1.4
Requires:       numpy 
Requires:       python-pillow
Requires:       mlt-python
Requires:       cairomm
Requires:       pyxdg
Requires:       gtk3

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
%setup -qn %{name}-%{commit0}/flowblade-trunk
# fix to  /usr/bin/flowblade
%patch0 -p1

# Fix script-without-shebang erros in fedora-review
# Remove permission to execute in all files except files that have sheban.
find . -type f -executable | xargs chmod a-x
find . -type f | xargs grep -El '\#!/usr/bin/env' | xargs chmod a+x

# fix to %%{_datadir}/locale
sed -i "s|respaths.LOCALE_PATH|'%{_datadir}/locale'|g" Flowblade/translations.py

%build 
python setup.py build

%install 
python setup.py install --skip-build --root %{buildroot} 

#package_data files lose executable permissions fix it again.
chmod +x %{buildroot}%{python_sitelib}/Flowblade/launch/*

# setup of mime is already done, so for what we need this file ?
%{__rm} %{buildroot}/usr/lib/mime/packages/flowblade

# move .mo files to /usr/share/locale the right place
for i in $(ls -d %{buildroot}%{python_sitelib}/Flowblade/locale/*/LC_MESSAGES/ | sed 's/\(^.*locale\/\)\(.*\)\(\/LC_MESSAGES\/$\)/\2/') ; do
    mkdir -p %{buildroot}%{_datadir}/locale/$i/LC_MESSAGES/
    mv %{buildroot}%{python_sitelib}/Flowblade/locale/$i/LC_MESSAGES/%{name}.mo \
        %{buildroot}%{_datadir}/locale/$i/LC_MESSAGES/
done
%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc README
%license COPYING
%{_bindir}/flowblade
%{_datadir}/applications/flowblade.desktop
%{_mandir}/man1/flowblade.1.gz
%{_datadir}/mime
%{_datadir}/pixmaps/flowblade.png
%{python_sitelib}/Flowblade/
%{python_sitelib}/flowblade*

%changelog
* Mon Aug 01 2016 Sérgio Basto <sergio@serjux.com> - 1.6.0-3.gitc847b32
-
  https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

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
- Remove /usr/lib/mime/packages/flowblade file 
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

