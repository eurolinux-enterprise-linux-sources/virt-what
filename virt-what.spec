Name:           virt-what
Version:        1.11
Release:        1.3%{?dist}
Summary:        Detect if we are running in a virtual machine

Group:          Applications/Emulators
License:        GPLv2+
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

URL:            http://people.redhat.com/~rjones/virt-what/
Source0:        http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz

# These patches are kept in the upstream git repo, in the rhel-6.9 branch.
# http://git.annexia.org/?p=virt-what.git;a=shortlog;h=refs/heads/rhel-6.9
Patch0001: 0001-IA64-Xen-HVM-should-print-xen-hvm-not-xen-domU.patch
Patch0002: 0002-Preserve-ebx-across-CPUID-when-using-PIE-thanks-Faus.patch
Patch0003: 0003-doc-Add-note-about-use-of-this-tool-for-system-tunin.patch
Patch0004: 0004-man-detect-with-autotools-if-pod2man-is-present.patch
Patch0005: 0005-Remove-bash-backtick-command-substitution.patch
Patch0006: 0006-Disallow-use-of-unset-variables.patch
Patch0007: 0007-Retire-private-id-executables.patch
Patch0008: 0008-Update-GNU-license-FSF-address.patch
Patch0009: 0009-Change-dmidecode-detection-of-Hitachi-Virtage.patch
Patch0010: 0010-Direct-output-from-fail-to-stderr.patch
Patch0011: 0011-Add-detection-for-LXC-tests.patch
Patch0012: 0012-Remove-reference-to-sbin-id-from-Makefile.patch
Patch0013: 0013-Be-consistent-with-variable-quoting-and-braces.patch
Patch0014: 0014-Add-lxc-to-virt-what-man-page.patch
Patch0015: 0015-Ignore-automake-parallel-test-files.patch
Patch0016: 0016-Differentiate-between-vserver-host-and-guest.patch
Patch0017: 0017-Detect-new-Xen-VMs-RHBZ-973663.patch
Patch0018: 0018-xen-Don-t-emit-warning-message-if-proc-xen-capabilit.patch
Patch0019: 0019-Fix-various-typos-and-mistakes-in-comments.patch
Patch0020: 0020-Fix-spelling-mistake-in-the-man-page-RHBZ-1099289.patch
Patch0021: 0021-Added-check-and-test-routines-for-Docker.patch
Patch0022: 0022-Added-documentation-for-Docker-tests.patch
Patch0023: 0023-virt-what.in-remove-bash-ism.patch
Patch0024: 0024-virt-what.in-get-effective-uid-in-a-portable-way.patch
Patch0025: 0025-virt-what.in-warn-about-missing-cpuid-virt-helper-pr.patch
Patch0026: 0026-virt-what.in-verify-files-exists-before-grepping-the.patch
Patch0027: 0027-virt-what.in-make-option-processing-portable.patch
Patch0028: 0028-build-use-portable-Makefile-variables.patch
Patch0029: 0029-Add-space-before-parens-in-function-defns-for-readab.patch
Patch0030: 0030-Add-lkvm-detection.patch
Patch0031: 0031-Add-ARM-support.patch
Patch0032: 0032-xen-arm-Fix-path-in-EXTRA_DIST.patch
Patch0033: 0033-Update-copyright-years.patch
Patch0034: 0034-Add-QEMU-KVM-detection-for-ACPI-boot-ARM.patch
Patch0035: 0035-trivial-comment-fixup.patch
Patch0036: 0036-Add-oVirt-RHBZ-1249438.patch
Patch0037: 0037-trivial-virt-what.in-doesn-t-use-tabs.patch
Patch0038: 0038-qemu-kvm-try-dmidecode-on-all-targets.patch
Patch0039: 0039-qemu-kvm-dmidecode-look-for-KVM.patch
Patch0040: 0040-Add-support-for-detecting-ppc64-LPAR-as-virt-guests.patch
Patch0041: 0041-Update-the-previous-commit-to-use-system-virt-standa.patch
Patch0042: 0042-Add-detection-of-Red-Hat-Enterprise-Virtualization-h.patch
Patch0043: 0043-Add-detection-of-bhyve-FreeBSD-hypervisor.patch
Patch0044: 0044-Add-documentation-for-bhyve.patch

# This is provided by the build root, but we make it explicit
# anyway in case this was dropped from the build root in future.
BuildRequires:  /usr/bin/pod2man

# Required at build time in order to do 'make check' (for getopt).
BuildRequires:  util-linux-ng

# git is used for patch management.  Since some patches touch autoconf
# files, we must also install autotools.
BuildRequires:  git
BuildRequires:  autoconf
BuildRequires:  automake

# Because .gitignore is not included in the tarball, we have to
# include it here.
Source1:        dot-gitignore

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
cp %{SOURCE1} .gitignore
git init
git config user.email "rjones@redhat.com"
git config user.name "virt-what"
git add .
git commit -a -q -m "%{version} baseline"
git am %{patches}


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
* Mon Oct 31 2016 Richard W.M. Jones <rjones@redhat.com> - 1.11-1.3
- Add all patches from 1.11 to upstream 1.15+.
  resolves: rhbz#1249439 rhbz#1312431

* Thu Oct 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.11-1.2
- Add patch to fix dmidecode detection of Hitachi Virtage
  (thanks Satoru Moriya, Masaki Kimura)
  resolves: rhbz#829427

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
