Name:           virt-what
Version:        1.13
Release:        8%{?dist}
Summary:        Detect if we are running in a virtual machine
License:        GPLv2+

URL:            http://people.redhat.com/~rjones/virt-what/
Source0:        http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz

# These patches are kept in the upstream git repo, in the rhel-7.3 branch.
# http://git.annexia.org/?p=virt-what.git;a=shortlog;h=refs/heads/rhel-7.3
Patch0001:      0001-Differentiate-between-vserver-host-and-guest.patch
Patch0002:      0002-Detect-new-Xen-VMs-RHBZ-973663.patch
Patch0003:      0003-xen-Don-t-emit-warning-message-if-proc-xen-capabilit.patch
Patch0004:      0004-Fix-various-typos-and-mistakes-in-comments.patch
Patch0005:      0005-Fix-spelling-mistake-in-the-man-page-RHBZ-1099289.patch
Patch0006:      0006-Added-check-and-test-routines-for-Docker.patch
Patch0007:      0007-Added-documentation-for-Docker-tests.patch
Patch0008:      0008-virt-what.in-remove-bash-ism.patch
Patch0009:      0009-virt-what.in-get-effective-uid-in-a-portable-way.patch
Patch0010:      0010-virt-what.in-warn-about-missing-cpuid-virt-helper-pr.patch
Patch0011:      0011-virt-what.in-verify-files-exists-before-grepping-the.patch
Patch0012:      0012-virt-what.in-make-option-processing-portable.patch
Patch0013:      0013-build-use-portable-Makefile-variables.patch
Patch0014:      0014-Add-space-before-parens-in-function-defns-for-readab.patch
Patch0015:      0015-Add-lkvm-detection.patch
Patch0016:      0016-Add-ARM-support.patch
Patch0017:      0017-xen-arm-Fix-path-in-EXTRA_DIST.patch
Patch0018:      0018-Update-copyright-years.patch
Patch0019:      0019-Add-QEMU-KVM-detection-for-ACPI-boot-ARM.patch
Patch0020:      0020-trivial-comment-fixup.patch
Patch0021:      0021-Add-oVirt-RHBZ-1249438.patch
Patch0022:      0022-trivial-virt-what.in-doesn-t-use-tabs.patch
Patch0023:      0023-qemu-kvm-try-dmidecode-on-all-targets.patch
Patch0024:      0024-qemu-kvm-dmidecode-look-for-KVM.patch
Patch0025:      0025-Add-support-for-detecting-ppc64-LPAR-as-virt-guests.patch
Patch0026:      0026-Update-the-previous-commit-to-use-system-virt-standa.patch

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
%ifarch aarch64 %{ix86} x86_64
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
* Wed Jul 27 2016 Richard W.M. Jones <rjones@redhat.com> - 1.13-8
- Depend on dmidecode on aarch64
  resolves: rhbz#1360699

* Mon Jun 20 2016 Richard W.M. Jones <rjones@redhat.com> - 1.13-7
- Add support for detecting POWER KVM and LPAR
  resolves: rhbz#1147876
- Detect RHEV/oVirt
  resolves: rhbz#1249438
- Detect ACPI boot aarch64 guest
  resolves: rhbz#1275349
- Fix typo in manual page
  resolves: rhbz#1099289

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
