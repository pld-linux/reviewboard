Summary:	Web-based code review tool
Name:		ReviewBoard
Version:	1.5.3
Release:	0.1
License:	MIT
Group:		Applications/Networking
URL:		http://www.review-board.org
Source0:	http://downloads.review-board.org/releases/ReviewBoard/1.5/%{name}-%{version}.tar.gz
# Source0-md5:	735148b8c865d77b461a0cf80b72a1e7
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	django-evolution >= 0.6.2
Requires:	httpd
Requires:	patchutils
Requires:	python-PIL
Requires:	python-dateutil
Requires:	python-django >= 1.1.3
Requires:	python-djblets >= 0.6.7
Requires:	python-flup
Requires:	python-memcached
Requires:	python-nose
Requires:	python-paramiko
Requires:	python-pygments >= 1.1.1
Requires:	python-pysvn
Requires:	python-pytz
Requires:	python-recaptcha
Requires:	python-sqlite
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Review Board is a powerful web-based code review tool that offers
developers an easy way to handle code reviews. It scales well from
small projects to large companies and offers a variety of tools to
take much of the stress and time out of the code review process.

%prep
%setup -q
%{__sed} -i -e 's/^from ez_setup/#from ez_setup/' setup.py
%{__sed} -i -e 's/^use_setuptools()/#use_setuptools()/' setup.py
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' reviewboard/manage.py

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
# --skip-build causes bad stuff in siteconfig.py as of 0.8.4
%{__python} setup.py install \
	--skip-build \
	--root $RPM_BUILD_ROOT

%py_postclean

# scripts that have a shebang and are meaningful to run; make executable:
# need to reinstall as py_postclean has removed .py
install -p reviewboard/manage.py $RPM_BUILD_ROOT%{py_sitescriptdir}/reviewboard/manage.py

# Remove test data from the installed packages
rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/reviewboard/diffviewer/testdata \
       $RPM_BUILD_ROOT%{py_sitescriptdir}/reviewboard/scmtools/testdata

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# The rb-site executable has a PyGTK GUI, so would normally
# require us to ship a .desktop file.  However it can only be run when supplied
# a directory as a command-line argument, hence it wouldn't be meaningful to
# create a .desktop file for it.
%doc AUTHORS COPYING INSTALL NEWS README
%attr(755,root,root) %{_bindir}/rb-site
%attr(755,root,root) %{_bindir}/rbssh
%dir %{py_sitescriptdir}/reviewboard
%{py_sitescriptdir}/reviewboard/nose.cfg
%{py_sitescriptdir}/reviewboard/accounts
%{py_sitescriptdir}/reviewboard/admin
%{py_sitescriptdir}/reviewboard/changedescs
%{py_sitescriptdir}/reviewboard/diffviewer
%{py_sitescriptdir}/reviewboard/htdocs
%{py_sitescriptdir}/reviewboard/iphone
%{py_sitescriptdir}/reviewboard/notifications
%{py_sitescriptdir}/reviewboard/reports
%{py_sitescriptdir}/reviewboard/reviews
%{py_sitescriptdir}/reviewboard/scmtools
%{py_sitescriptdir}/reviewboard/templates
%{py_sitescriptdir}/reviewboard/webapi
%{py_sitescriptdir}/reviewboard/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/reviewboard/manage.py
%{py_sitescriptdir}/reviewboard/cmdline
%{py_sitescriptdir}/webtests/*.py*
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/ReviewBoard-%{version}-*.egg-info
%endif
