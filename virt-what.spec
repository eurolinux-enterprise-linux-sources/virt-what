Name:           virt-what
Version:        1.11
Release:        1.1%{?dist}
Summary:        Detect if we are running in a virtual machine

Group:          Applications/Emulators
License:        GPLv2+
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

URL:            http://people.redhat.com/~rjones/virt-what/
Source0:        http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz

# Patches over upstream 1.11.
Patch0001:      0001-IA64-Xen-HVM-should-print-xen-hvm-not-xen-domU.patch

# This is provided by the build root, but we make it explicit
# anyway in case this was dropped from the build root in future.
BuildRequires:  /usr/bin/pod2man

# Required at build time in order to do 'make check' (for getopt).
BuildRequires:  util-linux-ng

# virt-what script uses dmidecode and getopt (from util-linux-ng).
# RPM cannot detect this so make the dependencies explicit here.
%ifarch %{ix86} x86_64 ia64
Requires:       dmidecode
%endif
%if 0%{?rhel} >= 6
Requires:       util-linux-ng
%endif


%description
virt-what is a shell script which can be used to detect if the program
is running in a virtual machine.

The program prints out a list of "facts" about the virtual machine,
derived from heuristics.  One fact is printed per line.

If nothing is printed and the script exits with code 0 (no error),
then it can mean either that the program is running on bare-metal or
the program is running inside a type of virtual machine which we don't
know about or cannot detect.

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

%patch0001 -p1


%build
%configure
make


%check
make check


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_sbindir}/virt-what
%{_libexecdir}/virt-what-cpuid-helper
%{_mandir}/man1/*.1*


%changelog
* Fri Jun 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1.11-1.1
- Rebase to virt-what 1.11.
  resolves: rhbz#672211
- Add patch "IA64 Xen HVM should print 'xen-hvm' not 'xen-domU'" from upstream.

* Mon Jan 31 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3-4.4
- Various improvements to the wording in the manual page.
  resolves: rhbz#672285
- Confirm support for Microsoft HyperV and add a regression test.
  resolves: rhbz#670272

* Mon Jan 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3-4.3
- Don't depend on util-linux-ng on RHEL 5.

* Mon Jan 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3-4.2
- Add support for Microsoft HyperV (RHBZ#670272).
- Add support for Hitachi Virtage (RHBZ#670530).
- Add support for EC2 (Xen) instances (RHBZ#671126).  This includes
  backporting the test framework and enabling tests.
- Add support for IBM Systemz z/VM, LPAR (RHBZ#671132).

* Mon Jan 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3-4.1
- Add support for IBM PowerVM Lx86 Linux/x86 emulator (RHBZ#668857).
- Move configure into build (not prep).

* Tue Dec 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-4
- Rebuild on all architectures.

* Thu Oct 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-3
- Initial import into Fedora.

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- Make changes suggested by reviewer (RHBZ#644259).

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- Initial release.
