%define		mod_name	ruid2
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: run all httpd process under user's access right
Summary(pl.UTF-8):	Moduł do apache: uruchamiania procesów httpd na prawach użytkowniów
Name:		apache-mod_%{mod_name}
Version:	0.9.4
Release:	0.1
License:	ASL v2.0
Group:		Networking/Daemons/HTTP
Source0:	http://sourceforge.net/projects/mod-ruid/files/mod_ruid2/mod_%{mod_name}-%{version}.tar.bz2
# Source0-md5:	23e43b818c578142689de4d36868391a
Source1:	mod_%{mod_name}.conf
URL:		http://mod-ruid.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	libcap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
With this module, all httpd process run under user's access right,
not nobody or http.  mod_ruid2 makes use of kernel capabilites
and after receiving a new request suids again. If you want to run
apache modules, i.e. WebDAV, PHP, and so on under user's right,
this module is useful. 

%description -l pl.UTF-8
Przy pomocy tego modułu wszystkie procesy httpd są uruchamiane na
prawach użytkowników zamiast nobody czy http. mod_ruid2 wykorzystuje
implementację "capability" jądra linuksa do zmiany właściciela
procesu.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -l cap -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
