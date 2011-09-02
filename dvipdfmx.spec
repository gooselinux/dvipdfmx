
# These macros need to match what is in the texlive-texmf package. For
# this reason texlive-texmf is a BuildRequires, and it installs an rpm
# macro file that defines them. Here we define them in case they're
# not set.
%{!?_texmf_main: %define _texmf_main %{_datadir}/texmf}
%{!?_texmf_conf: %define _texmf_conf %{_sysconfdir}/texmf}

%define snapshot 20090708

Name:           dvipdfmx
Version:        0
Release:        0.31.%{snapshot}cvs%{?dist}
Summary:        A DVI to PDF translator

Group:          Applications/Publishing
License:        GPLv2+
URL:            http://project.ktug.or.kr/dvipdfmx/
Source0:        http://project.ktug.or.kr/dvipdfmx/snapshot/latest/%{name}-%{snapshot}.tar.gz

# This patch not accepted upstream, but is to avoid a filename conflict with
# ebb from the dvipdfm package. Long term we should just drop the dvipdfm package.
Patch0:	       dvipdfmx-20090708-ebb-to-ebbx.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kpathsea-devel libpng-devel zlib-devel libpaper-devel texlive-texmf
Requires:       texlive-texmf-fonts
Requires:       ghostscript
Requires(post): /usr/bin/mktexlsr
Requires(postun): /usr/bin/mktexlsr

%description
The dvipdfmx (formerly dvipdfm-cjk) project provides an eXtended version
of the dvipdfm, a DVI to PDF translator developed by Mark A. Wicks.

The primary goal of this project is to support multi-byte character
encodings and large character sets for East Asian languages. The secondary
goal is to support as many features as pdfTeX developed by Han The Thanh.

This project is a combined work of the dvipdfm-jpn project by Shunsaku
Hirata and its modified one, dvipdfm-kor, by Jin-Hwan Cho.


%prep
%setup -q -n %{name}-%{snapshot}
%patch0 -p1 -b ebb-to-ebbx

%build
%configure
make %{?_smp_mflags}

# create customized cid-x.map for dvipdfmx (#418091)
cat <<EOF >> cid-x.map
%%
%% ASCII pTeX Examples
%%

%% Ryumin and GothicBBB found in PostScript printers:
rml  H !Ryumin-Light
gbm  H !GothicBBB-Medium
rmlv V !Ryumin-Light
gbmv V !GothicBBB-Medium
EOF


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

mkdir -p %{buildroot}%{_texmf_conf}/dvipdfmx
mv cid-x.map %{buildroot}%{_texmf_conf}/dvipdfmx/


%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/mktexlsr > /dev/null 2>&1 || :

%postun
/usr/bin/mktexlsr > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/dvipdfmx
%{_bindir}/extractbb
%{_bindir}/ebbx
%dir %{_texmf_conf}/dvipdfmx/
%config(noreplace) %{_texmf_conf}/dvipdfmx/cid-x.map
%{_texmf_main}/dvipdfmx
%{_texmf_main}/fonts/map/dvipdfmx/cid-x.map
%{_texmf_main}/fonts/map/glyphlist/glyphlist.txt
%{_texmf_main}/fonts/map/glyphlist/pdfglyphlist.txt
%{_texmf_main}/fonts/cmap/dvipdfmx/EUC-UCS2


%changelog
* Tue Jan 12 2010 Jindrich Novy <jnovy@redhat.com> - 0-0.31.20090708cvs
- fix source URL
Related: #543948

* Mon Sep 15 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.30.20090708cvs
- Add dvipdfmx-20090708-ebb-to-ebbx.patch to rename ebb to ebbx to avoid file
  conflict with ebb package

* Mon Sep 15 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.29.20090708cvs
- Fix up errors in file list

* Fri Sep 11 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.28.20090708cvs
- Update to 20090708 snapshot to fix BZ 519672
- Remove dvipdfmx-20080617-ebb-to-ebbx.patch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.27.20090115cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.26.20090115cvs
- Update to 20090115 snapshot

* Tue Jun 17 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.25.20080617cvs
- Rework ebb-to-ebbx patch for latest CVS snapshot
- Fix files section
 
* Tue Jun 17 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.24.20080617cvs
- Update to 20080617 CVS snapshot

* Sun May 26 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.23.20080520cvs
- Added dvipdfmx-20080520-ebb-to-ebbx.patch to rename ebb to ebbx to stop
  conflict with dvipdfm package (BZ #448347)

* Tue May 20 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.22.20080520cvs
- Bump release to fix broken CVS tag
- Correct email address in spec file changelog

* Tue May 20 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.21.20080520cvs
- Update to snapshot 20080520
- Move config to dvipdfmx directory (rather than dvipdfm) as required by this snapshot

* Sun Feb 17 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0-0.20.20071115cvs
- Remove obsolete and Provides for dvipdfm
- Explicitly list contents of bindir in file list
- Fix version and release tags to be guideline conforming
- Add INSTALL='install -p' to make install
- Add macro definitions from texlive-texmf spec file in case not defined
- Remove NEWS and TODO from doc file list

* Sun Feb 17 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 20071115-1
- Initial separate package - formerly part of texlive

