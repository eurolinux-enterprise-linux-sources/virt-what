Name:           virt-what
Version:        1.13
Release:        6%{?dist}
Summary:        Detect if we are running in a virtual machine
License:        GPLv2+

URL:            http://people.redhat.com/~rjones/virt-what/
Source0:        http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz

Patch1:         0001-Differentiate-between-vserver-host-and-guest.patch
Patch2:         0002-Detect-new-Xen-VMs-RHBZ-973663.patch
Patch3:         0001-xen-Don-t-emit-warning-message-if-proc-xen-capabilit.patch
Patch4:         0001-Fix-various-typos-and-mistakes-in-comments.patch
Patch5:         0003-Fix-spelling-mistake-in-the-man-page-RHBZ-1099289.patch
Patch6:         0004-Added-check-and-test-routines-for-Docker.patch
Patch7:         0005-Added-documentation-for-Docker-tests.patch
Patch8:         0006-virt-what.in-remove-bash-ism.patch
Patch9:         0007-virt-what.in-get-effective-uid-in-a-portable-way.patch
Patch10:        0008-virt-what.in-warn-about-missing-cpuid-virt-helper-pr.patch
Patch11:        0009-virt-what.in-verify-files-exists-before-grepping-the.patch
Patch12:        0010-virt-what.in-make-option-processing-portable.patch
Patch13:        0011-build-use-portable-Makefile-variables.patch
Patch14:        0012-Add-space-before-parens-in-function-defns-for-readab.patch
Patch15:        0013-Add-lkvm-detection.patch
Patch16:        0014-Add-ARM-support.patch
Patch17:        0015-xen-arm-Fix-path-in-EXTRA_DIST.patch


# This is provided by the build root, but we make it explicit
# anyway in case this was dropped from the build root in future.
BuildRequires:  /usr/bin/pod2man

# Required at build time in order to do 'make check' (for getopt).
BuildRequires:  util-linux

# git is used for patch management.  Since some patches touch autoconf
# files, we must also install autotools.
BuildRequires:  git
BuildRequires:  autoconf
BuildRequires:  automake

# virt-what script uses dmidecode and getopt (from util-linux).
# RPM cannot detect this so make the dependencies explicit here.
%ifarch %{ix86} x86_64
Requires:       dmidecode
%endif
Requires:       util-linux


%description
virt-what is a shell script which can be used to detect if the program
is running in a virtual machine.

The program prints out a list of "facts" about the virtual machine,
derived from heuristics.  One fact is printed per line.

If nothing is printed and the script exits with code 0 (no error),
then it can mean either that the program is running on bare-metal or
the program is running inside a type of virtual machine which we don't
know about or can't detect.

Current types of virtualization detected:

 - hyperv       Microsoft Hyper-V
 - kvm          Linux Kernel Virtual Machine (KVM)
 - openvz       OpenVZ or Virtuozzo
 - powervm_lx86 IBM PowerVM Lx86 Linux/x86 emulator
 - qemu         QEMU (unaccelerated)
 - uml          User-Mode Linux (UML)
 - virtage      Hitachi Virtualization Manager (HVM) Virtage LPAR
 - virtualbox   VirtualBox
 - virtualpc    Microsoft VirtualPC
 - vmware       VMware
 - xen          Xen
 - xen-dom0     Xen dom0 (privileged domain)
 - xen-domU     Xen domU (paravirtualized guest domain)
 - xen-hvm      Xen guest fully virtualized (HVM)


%prep
%setup -q

# Use git to manage patches.
# http://rwmj.wordpress.com/2011/08/09/nice-rpm-git-patch-management-trick/
git init
git config user.email "rjones@redhat.com"
git config user.name "virt-what"
git add .
git commit -a -q -m "%{version} baseline"
git am %{patches}


%build
%configure
make


%install
make install DESTDIR=$RPM_BUILD_ROOT


%check
make check


%files
%doc README COPYING
%{_sbindir}/virt-what
%{_libexecdir}/virt-what-cpuid-helper
%{_mandir}/man1/*.1*


%changelog
* Tue Apr 21 2015 Richard W.M. Jones <rjones@redhat.com> - 1.13-6
- Fix detection of aarch64
  resolves: rhbz#1201845
  Add all commits to version 1.15.

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.13-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.13-4
- Mass rebuild 2013-12-27

* Mon Oct 28 2013 Richard W.M. Jones <rjones@redhat.com> - 1.13-3
- Suppress warning message on Amazon EC2:
  "grep: /proc/xen/capabilities: No such file or directory"

* Wed Sep 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1.13-2
- Include two upstream patches for detecting Xen and Linux VServer better
  (RHBZ#973663).
- Modernize the spec file.

* Mon Jul 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1.13-1
- New upstream version 1.13.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1.12-1
- New upstream version 1.12.

* Wed Feb 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.11-3
- Remove ExclusiveArch, but don't require dmidecode except on
  i?86 and x86-64 (RHBZ#791370).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 27 2011 Richard W.M. Jones <rjones@redhat.com> - 1.11-1
- New upstream version 1.11.

* Wed May 25 2011 Richard W.M. Jones <rjones@redhat.com> - 1.10-1
- New upstream version 1.10.

* Tue Mar  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1.9-1
- New upstream version 1.9.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Richard W.M. Jones <rjones@redhat.com> - 1.8-1
- New upstream version 1.8.

* Thu Jan 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1.7-1
- New upstream version 1.7.

* Wed Jan 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1.6-2
- New upstream version 1.6.
- BuildRequires 'getopt' from util-linux-ng.

* Tue Jan 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1.5-1
- New upstream version 1.5.
- Add 'make check' section.

* Tue Jan 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1.4-1
- New upstream version 1.4.
- More hypervisor types detected.

* Thu Oct 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-4
- Move configure into build (not prep).

* Thu Oct 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-3
- Initial import into Fedora.

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- Make changes suggested by reviewer (RHBZ#644259).

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- Initial release.
