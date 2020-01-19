Name:           virt-what
Version:        1.18
Release:        4%{?dist}
Summary:        Detect if we are running in a virtual machine
License:        GPLv2+

URL:            http://people.redhat.com/~rjones/virt-what/
Source0:        http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz

# Patches from upstream since 1.18 was released.
Patch0001:      0001-Missing-have_cpuinfo-check.patch
Patch0002:      0002-Remove-bashisms.patch
Patch0003:      0003-As-xen-pv-guest-can-access-cpuid-from-Intel-CPUs-sta.patch
Patch0004:      0004-Recognize-ppc64le-little-endian-virtualization-RHBZ-.patch

# This is provided by the build root, but we make it explicit
# anyway in case this was dropped from the build root in future.
BuildRequires:  /usr/bin/pod2man

# Required at build time in order to do 'make check' (for getopt).
BuildRequires:  util-linux

# virt-what script uses dmidecode and getopt (from util-linux).
# RPM cannot detect this so make the dependencies explicit here.
%ifarch aarch64 %{ix86} x86_64
Requires:       dmidecode
%endif
Requires:       util-linux

# Runs the 'which' program to find the helper.
Requires:       which


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

 - aws          Amazon Web Services cloud guest
 - bhyve        FreeBSD hypervisor
 - docker       Docker container
 - hyperv       Microsoft Hyper-V
 - ibm_power-kvm
                IBM POWER KVM
 - ibm_power-lpar_shared
 - ibm_power-lpar_dedicated
                IBM POWER LPAR (hardware partition)
 - ibm_systemz-*
                IBM SystemZ Direct / LPAR / z/VM / KVM
 - ldoms        Oracle VM Server for SPARC Logical Domains
 - linux_vserver
                Linux VServer container
 - lxc          Linux LXC container
 - kvm          Linux Kernel Virtual Machine (KVM)
 - lkvm         LKVM / kvmtool
 - openvz       OpenVZ or Virtuozzo
 - ovirt        oVirt node
 - parallels    Parallels Virtual Platform
 - powervm_lx86 IBM PowerVM Lx86 Linux/x86 emulator
 - qemu         QEMU (unaccelerated)
 - rhev         Red Hat Enterprise Virtualization
 - uml          User-Mode Linux (UML)
 - virtage      Hitachi Virtualization Manager (HVM) Virtage LPAR
 - virtualbox   VirtualBox
 - virtualpc    Microsoft VirtualPC
 - vmm          vmm OpenBSD hypervisor
 - vmware       VMware
 - xen          Xen
 - xen-dom0     Xen dom0 (privileged domain)
 - xen-domU     Xen domU (paravirtualized guest domain)
 - xen-hvm      Xen guest fully virtualized (HVM)


%prep
%setup -q
%autopatch -p1


%build
%configure
make


%install
make install DESTDIR=$RPM_BUILD_ROOT


%check
if ! make check ; then
    cat test-suite.log
    exit 1
fi

%files
%doc README COPYING
%{_sbindir}/virt-what
%{_libexecdir}/virt-what-cpuid-helper
%{_mandir}/man1/*.1*


%changelog
* Tue Oct 17 2017 Richard W.M. Jones <rjones@redhat.com> - 1.18-4
- Add patch to recognize ppc64le virtualization.
  resolves: rhbz#1147876

* Tue Oct 17 2017 Richard W.M. Jones <rjones@redhat.com> - 1.18-2
- Rebase to Fedora Rawhide / upstream version.
- Include upstream patches since 1.18 was released.
  resolves: rhbz#1476878

* Tue Mar 28 2017 Richard W.M. Jones <rjones@redhat.com> - 1.13-10
- Require 'which' program
  resolves: rhbz#1433005

* Thu Feb 16 2017 Richard W.M. Jones <rjones@redhat.com> - 1.13-9
- Detect RHEV/oVirt (second fix)
  resolves: rhbz#1249438

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
