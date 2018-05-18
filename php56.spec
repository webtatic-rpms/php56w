%if 0%{?scl:1}
%scl_package php
%global _name          %{name}
%else
%global _name          php
%global pkg_name       %{name}
%global _root_sysconfdir  %{_sysconfdir}
%global _root_bindir      %{_bindir}
%global _root_sbindir     %{_sbindir}
%global _root_includedir  %{_includedir}
%global _root_libdir      %{_libdir}
%global _root_prefix      %{_prefix}
%global _root_initddir    %{_initrddir}
%endif

# API/ABI check
%global apiver      20131106
%global zendver     20131226
%global pdover      20080721
# Extension version
%global fileinfover 1.0.5
%global pharver     2.0.2
%global zipver      1.12.5
%global jsonver     1.2.1
%global opcachever  7.0.6-dev

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for minor release purposes
%global minor_release 5.6

 # version used for php embedded library soname
%global embed_version %{minor_release}

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %{expand: %%global runselftest 1}}

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_root_libdir}/mysql/mysql_config

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global with_tmpfiles 1
%global _macrosdir %{_rpmconfigdir}/macros.d
%else
%global with_tmpfiles 0
%global _macrosdir %{_root_sysconfdir}/rpm
%endif

%ifarch %{ix86} x86_64
%global with_fpm 1
%else
%global with_fpm 0
%endif

# Build mysql/mysqli/pdo extensions using libmysqlclient or only mysqlnd
%global with_libmysql 1

# Build ZTS extension or only NTS
%global with_zts      1

%global with_dtrace 1

# Build phpdbg
%global with_phpdbg   1

%if 0%{?__isa_bits:1}
%global isasuffix -%{__isa_bits}
%else
%global isasuffix %nil
%endif

# Ugly hack. Harcoded values to avoid relocation.
%global _httpd_mmn         %(cat %{_root_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)
%global _httpd_confdir     %{_root_sysconfdir}/httpd/conf.d
%global _httpd_moddir      %{_libdir}/httpd/modules
%global _root_httpd_moddir %{_root_libdir}/httpd/modules
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
# httpd 2.4 values
%global _httpd_apxs        %{_root_bindir}/apxs
%global _httpd_modconfdir  %{_root_sysconfdir}/httpd/conf.modules.d
%global _httpd_contentdir  /usr/share/httpd
%else
# httpd 2.2 values
%global _httpd_apxs        %{_root_sbindir}/apxs
%global _httpd_modconfdir  %{_root_sysconfdir}/httpd/conf.d
%global _httpd_contentdir  /var/www
%endif

%global with_zip     1
%global with_libzip  0
%global zipmod       zip

%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%global db_devel  db4-devel
%else
%global db_devel  libdb-devel
%endif

Summary: PHP scripting language for creating dynamic web sites
%if 0%{?scl:1}
Name: %{?scl_prefix}php
%else
Name: php56w
%endif
Version: 5.6.36
Release: 1%{?rcver:.%{rcver}}%{?dist}
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
License: PHP and Zend and BSD
Group: Development/Languages
URL: http://www.php.net/

Source0: https://secure.php.net/distributions/php-%{version}%{?rcver}.tar.bz2
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source8: php-fpm.sysconfig
Source9: php.modconf
Source10: php.ztsmodconf
Source11: php-fpm.init
Source50: opcache.ini
Source51: opcache-default.blacklist

# Build fixes
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-5.6.17-libdb.patch

# Fixes for extension modules

# Functional changes
Patch40: php-5.4.0-dlopen.patch
Patch42: php-5.6.13-systzdata-v13.patch
# See http://bugs.php.net/53436
Patch43: php-5.4.0-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-5.4.8-ldap_r.patch
# Make php_config.h constant across builds
Patch46: php-5.4.9-fixheader.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.4.9-phpinfo.patch
Patch48: php-5.5.0-icuconfig.patch
Patch49: php-5.5.19-curltlsconst.patch

# Fixes for tests

# Bug fixes

# Security fixes

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9, gmp-devel
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
BuildRequires: libstdc++-devel, openssl-devel
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
# For Sqlite3 extension
BuildRequires: sqlite-devel >= 3.6.0
%else
BuildRequires: sqlite-devel >= 3.0.0
%endif
BuildRequires: zlib-devel, pcre-devel >= 6.6, smtpdaemon, libedit-devel
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: libtool-ltdl-devel
%if %{with_libzip}
BuildRequires: libzip-devel >= 0.11
%endif
%{?scl:Requires: %scl_runtime}
Requires: httpd-mmn = %{_httpd_mmn}
Requires: %{name}-common%{?_isa} = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: %{name}-cli%{?_isa} = %{version}-%{release}
# For backwards-compatibility, require %{name}-cli for the time being:
Requires: %{name}-cli = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd

%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel
%endif
%if 0%{!?scl:1}
%if %{with_zts}
Provides: php-zts = %{version}-%{release}
Provides: php-zts%{?_isa} = %{version}-%{release}
%endif
Provides: php = %{version}-%{release}
Provides: php%{?_isa} = %{version}-%{release}
%endif
Provides: %{?scl_prefix}mod_php = %{version}-%{release}
%if %{with_zts}
Provides: %{name}-zts = %{version}-%{release}
Provides: %{name}-zts%{?_isa} = %{version}-%{release}
%endif

# Don't provides extensions, which are not shared library, as .so
%{?filter_provides_in: %filter_provides_in %{_libdir}/php/modules/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{_libdir}/php-zts/modules/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. 

The %{name} package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
Provides: php-cgi = %{version}-%{release}, php-cgi%{?_isa} = %{version}-%{release}
Provides: php-pcntl, php-pcntl%{?_isa}
Provides: php-readline, php-readline%{?_isa}
# Additional Provides for this package name
Provides: php-cli = %{version}-%{release}
Provides: php-cli%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-cgi = %{version}-%{release}, %{name}-cgi%{?_isa} = %{version}-%{release}
Provides: %{name}-pcntl, %{name}-pcntl%{?_isa}
Provides: %{name}-readline, %{name}-readline%{?_isa}

%description cli
The %{name}-cli package contains the command-line interface 
executing PHP scripts, /usr/bin/php, and the CGI interface.

%if %{with_phpdbg}
%package phpdbg
Group: Development/Languages
Summary: Interactive PHP debugger
BuildRequires: readline-devel
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
Provides: php-phpdbg = %{version}-%{release}
Provides: php-phpdbg%{?_isa} = %{version}-%{release}
%endif

%description phpdbg
Implemented as a SAPI module, phpdbg can excert complete control over
the environment without impacting the functionality or performance of
your code.

phpdbg aims to be a lightweight, powerful, easy to use debugging
platform for PHP
%endif

%if %{with_fpm}
%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM and fpm are licensed under BSD
License: PHP and Zend and BSD
%if %{with_systemd}
BuildRequires: systemd-devel
BuildRequires: systemd-units
Requires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
%endif
Requires(pre): /usr/sbin/useradd
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: libevent-devel >= 1.4.11
%if 0%{!?scl:1}
Provides: php-fpm = %{version}-%{release}
Provides: php-fpm%{?_isa} = %{version}-%{release}
%endif

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.
%endif

%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
License: PHP and BSD and ASL 1.0
# ABI/API check - Arch specific
Provides: %{?scl_prefix}php-api = %{apiver}%{isasuffix}, %{?scl_prefix}php-zend-abi = %{zendver}%{isasuffix}
Provides: %{?scl_prefix}php(api) = %{apiver}%{isasuffix}, %{?scl_prefix}php(zend-abi) = %{zendver}%{isasuffix}
Provides: %{?scl_prefix}php(language) = %{version}, %{?scl_prefix}php(language)%{?_isa} = %{version}
%if 0%{!?scl:1}
# Provides for all builtin/shared modules:
Provides: php-bz2, php-bz2%{?_isa}
Provides: php-calendar, php-calendar%{?_isa}
Provides: php-core = %{version}, php-core%{?_isa} = %{version}
Provides: php-ctype, php-ctype%{?_isa}
Provides: php-curl, php-curl%{?_isa}
Provides: php-date, php-date%{?_isa}
Provides: php-ereg, php-ereg%{?_isa}
Provides: php-exif, php-exif%{?_isa}
Provides: php-fileinfo, php-fileinfo%{?_isa}
Provides: php-pecl-Fileinfo = %{fileinfover}, php-pecl-Fileinfo%{?_isa} = %{fileinfover}
Provides: php-pecl(Fileinfo) = %{fileinfover}, php-pecl(Fileinfo)%{?_isa} = %{fileinfover}
Provides: php-filter, php-filter%{?_isa}
Provides: php-ftp, php-ftp%{?_isa}
Provides: php-gettext, php-gettext%{?_isa}
Provides: php-gmp, php-gmp%{?_isa}
Provides: php-hash, php-hash%{?_isa}
Provides: php-mhash = %{version}, php-mhash%{?_isa} = %{version}
Provides: php-iconv, php-iconv%{?_isa}
Provides: php-json, php-json%{?_isa}
Provides: php-pecl-json = %{jsonver}, php-pecl-json%{?_isa} = %{jsonver}
Provides: php-pecl(json) = %{jsonver}, php-pecl(json)%{?_isa} = %{jsonver}
Provides: php-libxml, php-libxml%{?_isa}
Provides: php-openssl, php-openssl%{?_isa}
Provides: php-pecl-phar = %{pharver}, php-pecl-phar%{?_isa} = %{pharver}
Provides: php-pecl(phar) = %{pharver}, php-pecl(phar)%{?_isa} = %{pharver}
Provides: php-phar, php-phar%{?_isa}
Provides: php-pcre, php-pcre%{?_isa}
Provides: php-reflection, php-reflection%{?_isa}
Provides: php-session, php-session%{?_isa}
Provides: php-shmop, php-shmop%{?_isa}
Provides: php-simplexml, php-simplexml%{?_isa}
Provides: php-sockets, php-sockets%{?_isa}
Provides: php-spl, php-spl%{?_isa}
Provides: php-standard = %{version}, php-standard%{?_isa} = %{version}
Provides: php-tokenizer, php-tokenizer%{?_isa}
%if %{with_zip}
Provides: php-zip, php-zip%{?_isa}
Provides: php-pecl-zip = %{zipver}, php-pecl-zip%{?_isa} = %{zipver}
Provides: php-pecl(zip) = %{zipver}, php-pecl(zip)%{?_isa} = %{zipver}
%endif
Provides: php-zlib, php-zlib%{?_isa}
# Additional Provides for this package name
Provides: php-common = %{version}-%{release}
Provides: php-common%{?_isa} = %{version}-%{release}
Conflicts: php-common < %{minor_release}
%endif
# Provides for all builtin/shared modules:
Provides: %{name}-bz2, %{name}-bz2%{?_isa}
Provides: %{name}-calendar, %{name}-calendar%{?_isa}
Provides: %{name}-core = %{version}, %{name}-core%{?_isa} = %{version}
Provides: %{name}-ctype, %{name}-ctype%{?_isa}
Provides: %{name}-curl, %{name}-curl%{?_isa}
Provides: %{name}-date, %{name}-date%{?_isa}
Provides: %{name}-ereg, %{name}-ereg%{?_isa}
Provides: %{name}-exif, %{name}-exif%{?_isa}
Provides: %{name}-fileinfo, %{name}-fileinfo%{?_isa}
Provides: %{name}-pecl-Fileinfo = %{fileinfover}, %{name}-pecl-Fileinfo%{?_isa} = %{fileinfover}
Provides: %{name}-pecl(Fileinfo) = %{fileinfover}, %{name}-pecl(Fileinfo)%{?_isa} = %{fileinfover}
Provides: %{name}-filter, %{name}-filter%{?_isa}
Provides: %{name}-ftp, %{name}-ftp%{?_isa}
Provides: %{name}-gettext, %{name}-gettext%{?_isa}
Provides: %{name}-gmp, %{name}-gmp%{?_isa}
Provides: %{name}-hash, %{name}-hash%{?_isa}
Provides: %{name}-mhash = %{version}, %{name}-mhash%{?_isa} = %{version}
Provides: %{name}-iconv, %{name}-iconv%{?_isa}
Provides: %{name}-json, %{name}-json%{?_isa}
Provides: %{name}-pecl-json = %{jsonver}, %{name}-pecl-json%{?_isa} = %{jsonver}
Provides: %{name}-pecl(json) = %{jsonver}, %{name}-pecl(json)%{?_isa} = %{jsonver}
Provides: %{name}-libxml, %{name}-libxml%{?_isa}
Provides: %{name}-openssl, %{name}-openssl%{?_isa}
Provides: %{name}-pecl-phar = %{pharver}, %{name}-pecl-phar%{?_isa} = %{pharver}
Provides: %{name}-pecl(phar) = %{pharver}, %{name}-pecl(phar)%{?_isa} = %{pharver}
Provides: %{name}-phar, %{name}-phar%{?_isa}
Provides: %{name}-pcre, %{name}-pcre%{?_isa}
Provides: %{name}-reflection, %{name}-reflection%{?_isa}
Provides: %{name}-session, %{name}-session%{?_isa}
Provides: %{name}-shmop, %{name}-shmop%{?_isa}
Provides: %{name}-simplexml, %{name}-simplexml%{?_isa}
Provides: %{name}-sockets, %{name}-sockets%{?_isa}
Provides: %{name}-spl, %{name}-spl%{?_isa}
Provides: %{name}-standard = %{version}, %{name}-standard%{?_isa} = %{version}
Provides: %{name}-tokenizer, %{name}-tokenizer%{?_isa}
%if %{with_zip}
Provides: %{name}-zip, %{name}-zip%{?_isa}
Provides: %{name}-pecl-zip = %{zipver}, %{name}-pecl-zip%{?_isa} = %{zipver}
Provides: %{name}-pecl(zip) = %{zipver}, %{name}-pecl(zip)%{?_isa} = %{zipver}
%endif
Provides: %{name}-zlib, %{name}-zlib%{?_isa}

%description common
The %{name}-common package contains files used by both the %{name}
package and the %{name}-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: %{name}-cli%{?_isa} = %{version}-%{release}, autoconf, automake
Requires: pcre-devel%{?_isa}
%if 0%{!?scl:1}
%if %{with_zts}
Provides: php-zts-devel = %{version}-%{release}
Provides: php-zts-devel%{?_isa} = %{version}-%{release}
%endif
Provides: php-devel = %{version}-%{release}
Provides: php-devel%{?_isa} = %{version}-%{release}
%endif
%if %{with_zts}
Provides: %{name}-zts-devel = %{version}-%{release}
Provides: %{name}-zts-devel%{?_isa} = %{version}-%{release}
%endif

%description devel
The %{name}-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: krb5-devel, openssl-devel, libc-client-devel
%if 0%{!?scl:1}
Provides: php-imap = %{version}-%{release}
Provides: php-imap%{?_isa} = %{version}-%{release}
%endif

%description imap
The %{name}-imap package contains a dynamic shared object that will
add support for the IMAP protocol to PHP.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel
%if 0%{!?scl:1}
Provides: php-ldap = %{version}-%{release}
Provides: php-ldap%{?_isa} = %{version}-%{release}
%endif

%description ldap
The %{name}-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
# ABI/API check - Arch specific
Provides: %{?scl_prefix}php-pdo-abi = %{pdover}%{isasuffix}
Provides: %{?scl_prefix}php(pdo-abi) = %{pdover}%{isasuffix}
%if 0%{!?scl:1}
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
Provides: php-sqlite3, php-sqlite3%{?_isa}
%endif
Provides: php-pdo_sqlite, php-pdo_sqlite3%{?_isa}
Provides: php-pdo = %{version}-%{release}
Provides: php-pdo%{?_isa} = %{version}-%{release}
%endif
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
Provides: %{name}-sqlite3, %{name}-sqlite3%{?_isa}
%endif
Provides: %{name}-pdo_sqlite, %{name}-pdo_sqlite%{?_isa}


%description pdo
The %{name}-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other 
databases.

%if %{with_libmysql}
%package mysql
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
BuildRequires: mysql-devel > 4.1.0
%else
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires: mysql-devel < 5.2
%else
BuildRequires: mysql-devel < 5.1
%endif
%endif
Requires: %{name}-pdo%{?_isa}
Provides: %{?scl_prefix}php_database
%if 0%{!?scl:1}
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
# Additional Provides for this package name
Provides: php-mysql = %{version}-%{release}
Provides: php-mysql%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-mysqli = %{version}-%{release}
Provides: %{name}-mysqli%{?_isa} = %{version}-%{release}
Provides: %{name}-pdo_mysql, php%{name}pdo_mysql%{?_isa}
Conflicts: %{name}-mysqlnd

%description mysql
The %{name}-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the %{name} package.
%endif

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-pdo%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php_database
%if 0%{!?scl:1}
Provides: php-mysql = %{version}-%{release}
Provides: php-mysql%{?_isa} = %{version}-%{release}
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
# Additional Provides for this package name
Provides: php-mysqlnd = %{version}-%{release}
Provides: php-mysqlnd%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-mysql = %{version}-%{release}
Provides: %{name}-mysql%{?_isa} = %{version}-%{release}
Provides: %{name}-mysqli = %{version}-%{release}
Provides: %{name}-mysqli%{?_isa} = %{version}-%{release}
Provides: %{name}-pdo_mysql, %{name}-pdo_mysql%{?_isa}

%if ! %{with_libmysql}
Obsoletes: %{name}-mysql < %{version}-%{release}
%endif

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: krb5-devel, openssl-devel, postgresql-devel
Requires: %{name}-pdo%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php_database
%if 0%{!?scl:1}
Provides: php-pdo_pgsql, php-pdo_pgsql%{?_isa}
# Additional Provides for this package name
Provides: php-pgsql = %{version}-%{release}
Provides: php-pgsql%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-pdo_pgsql, %{name}-pdo_pgsql%{?_isa}

%description pgsql
The %{name}-pgsql add PostgreSQL database support to PHP.
-PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
%{name} package.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
Provides: php-posix, php-posix%{?_isa}
Provides: php-sysvsem, php-sysvsem%{?_isa}
Provides: php-sysvshm, php-sysvshm%{?_isa}
Provides: php-sysvmsg, php-sysvmsg%{?_isa}
# Additional Provides for this package name
Provides: php-process = %{version}-%{release}
Provides: php-process%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-posix, %{name}-posix%{?_isa}
Provides: %{name}-sysvsem, %{name}-sysvsem%{?_isa}
Provides: %{name}-sysvshm, %{name}-sysvshm%{?_isa}
Provides: %{name}-sysvmsg, %{name}-sysvmsg%{?_isa}

%description process
The %{name}-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: %{name}-pdo%{?_isa} = %{version}-%{release}
BuildRequires: unixODBC-devel
Provides: %{?scl_prefix}php_database
%if 0%{!?scl:1}
Provides: php-pdo_odbc, php-pdo_odbc%{?_isa}
# Additional Provides for this package name
Provides: php-odbc = %{version}-%{release}
Provides: php-odbc%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-pdo_odbc, %{name}-pdo_odbc%{?_isa}

%description odbc
The %{name}-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the %{name}
package.

%package soap
Summary: A module for PHP applications that use the SOAP protocol
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: libxml2-devel
%if 0%{!?scl:1}
Provides: php-soap = %{version}-%{release}
Provides: php-soap%{?_isa} = %{version}-%{release}
%endif

%description soap
The %{name}-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%package interbase
Summary: A module for PHP applications that use Interbase/Firebird databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: firebird-devel
Requires: %{name}-pdo%{?_isa} = %{version}-%{release}
Provides: %{?scl_prefix}php_database
%if 0%{!?scl:1}
Provides: php-firebird = %{version}-%{release}
Provides: php-firebird%{?_isa} = %{version}-%{release}
Provides: php-pdo_firebird, php-pdo_firebird%{?_isa}
# Additional Provides for this package name
Provides: php-interbase = %{version}-%{release}
Provides: php-interbase%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-firebird = %{version}-%{release}
Provides: %{name}-firebird%{?_isa} = %{version}-%{release}
Provides: %{name}-pdo_firebird, %{name}-pdo_firebird%{?_isa}

%description interbase
The %{name}-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.

Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel
%if 0%{!?scl:1}
Provides: php-snmp = %{version}-%{release}
Provides: php-snmp%{?_isa} = %{version}-%{release}
%endif

%description snmp
The %{name}-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the %{name} package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
Provides: php-dom, php-dom%{?_isa}
Provides: php-xsl, php-xsl%{?_isa}
Provides: php-domxml, php-domxml%{?_isa}
Provides: php-wddx, php-wddx%{?_isa}
Provides: php-xmlreader, php-xmlreader%{?_isa}
Provides: php-xmlwriter, php-xmlwriter%{?_isa}
# Additional Provides for this package name
Provides: php-xml = %{version}-%{release}
Provides: php-xml%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-dom, %{name}-dom%{?_isa}
Provides: %{name}-xsl, %{name}-xsl%{?_isa}
Provides: %{name}-domxml, %{name}-domxml%{?_isa}
Provides: %{name}-wddx, %{name}-wddx%{?_isa}
Provides: %{name}-xmlreader, %{name}-xmlreader%{?_isa}
Provides: %{name}-xmlwriter, %{name}-xmlwriter%{?_isa}

%description xml
The %{name}-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libXMLRPC is licensed under BSD
License: PHP and BSD
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
Provides: php-xmlrpc = %{version}-%{release}
Provides: php-xmlrpc%{?_isa} = %{version}-%{release}
%endif

%description xmlrpc
The %{name}-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# onigurama is licensed under BSD
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and BSD and OpenLDAP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
Provides: php-mbstring = %{version}-%{release}
Provides: php-mbstring%{?_isa} = %{version}-%{release}
%endif

%description mbstring
The %{name}-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libgd is licensed under BSD
License: PHP and BSD
Requires: %{name}-common%{?_isa} = %{version}-%{release}
# Required to build the bundled GD library
BuildRequires: libjpeg-devel, libpng-devel, freetype-devel
BuildRequires: libXpm-devel, t1lib-devel
%if 0%{!?scl:1}
Provides: php-gd = %{version}-%{release}
Provides: php-gd%{?_isa} = %{version}-%{release}
%endif

%description gd
The %{name}-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
Provides: php-bcmath = %{version}-%{release}
Provides: php-bcmath%{?_isa} = %{version}-%{release}
%endif

%description bcmath
The %{name}-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: %{db_devel}, tokyocabinet-devel
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
Provides: php-dba = %{version}-%{release}
Provides: php-dba%{?_isa} = %{version}-%{release}
%endif

%description dba
The %{name}-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: libmcrypt-devel
%if 0%{!?scl:1}
Provides: php-mcrypt = %{version}-%{release}
Provides: php-mcrypt%{?_isa} = %{version}-%{release}
%endif

%description mcrypt
The %{name}-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel
%if 0%{!?scl:1}
Provides: php-tidy = %{version}-%{release}
Provides: php-tidy%{?_isa} = %{version}-%{release}
%endif

%description tidy
The %{name}-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package mssql
Summary: MSSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel
Provides: php_database
%if 0%{!?scl:1}
Provides: php-pdo_dblib, php-pdo_dblib%{?_isa}
# Additional Provides for this package name
Provides: php-mssql = %{version}-%{release}
Provides: php-mssql%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-pdo_dblib, %{name}-pdo_dblib%{?_isa}

%description mssql
The %{name}-mssql package contains a dynamic shared object that will
add MSSQL database support to PHP.  It uses the TDS (Tabular
DataStream) protocol through the freetds library, hence any
database server which supports TDS can be accessed.

%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}
Provides: php-embedded-devel%{?_isa} = %{version}-%{release}
# Additional Provides for this package name
Provides: php-embedded = %{version}-%{release}
Provides: php-embedded%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-embedded-devel = %{version}-%{release}
Provides: %{name}-embedded-devel%{?_isa} = %{version}-%{release}

%description embedded
The %{name}-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package opcache
Summary: An opcode cache Zend extension
Group: Development/Languages
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{!?scl:1}
# For obsoleted pecl extension
Provides: php-pecl-zendopcache = %{opcachever}, php-pecl-zendopcache%{?_isa} = %{opcachever}
Provides: php-pecl(OPcache) = %{opcachever}, php-pecl(OPcache) = %{opcachever}
# Additional Provides for this package name
Provides: php-opcache = %{version}-%{release}
Provides: php-opcache%{?_isa} = %{version}-%{release}
%endif
Provides: %{name}-pecl-zendopcache = %{opcachever}, %{name}-pecl-zendopcache%{?_isa} = %{opcachever}
Provides: %{name}-pecl(OPcache) = %{opcachever}, %{name}-pecl(OPcache) = %{opcachever}

%description opcache
The %{name}-opcache package contains an opcode cache used for caching and
optimizing intermediate code.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0
%if 0%{!?scl:1}
Provides: php-pspell = %{version}-%{release}
Provides: php-pspell%{?_isa} = %{version}-%{release}
%endif

%description pspell
The %{name}-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: recode-devel
%if 0%{!?scl:1}
Provides: php-recode = %{version}-%{release}
Provides: php-recode%{?_isa} = %{version}-%{release}
%endif

%description recode
The %{name}-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires: libicu-devel >= 4.0
%else
%if 0%{?scl:1}
BuildRequires: %{?scl_prefix}libicu-devel >= 4.0
%else
BuildRequires: libicu42-devel >= 4.0
%endif
%endif
%if 0%{!?scl:1}
Provides: php-intl = %{version}-%{release}
Provides: php-intl%{?_isa} = %{version}-%{release}
%endif

%description intl
The %{name}-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Enchant spelling extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.0
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4
%if 0%{!?scl:1}
Provides: php-enchant = %{version}-%{release}
Provides: php-enchant%{?_isa} = %{version}-%{release}
%endif

%description enchant
The %{name}-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.


%prep
%setup -q -n php-%{version}%{?rcver}
%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch8 -p1 -b .libdb

%patch40 -p1 -b .dlopen
%patch42 -p1 -b .systzdata
%patch43 -p1 -b .phpize
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif
%patch46 -p1 -b .fixheader
%patch47 -p1 -b .phpinfo
%patch48 -p1 -b .icuconfig
%if 0%{?rhel} >= 6
%patch49 -p1 -b .curltlsconst
%endif

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
cp ext/gd/libgd/README libgd_README
cp ext/gd/libgd/COPYING libgd_COPYING
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING

# Multiple builds for multiple SAPIs
mkdir build-cli build-apache build-embedded \
%if %{with_zts}
    build-zts build-ztscli \
%endif
%if %{with_fpm}
    build-fpm \
%endif
%if %{with_phpdbg}
    build-phpdbg
%endif

# ----- Manage known as failed test -------
# affected by systzdata patch
rm -f ext/date/tests/timezone_location_get.phpt
# fails sometime
rm -f ext/sockets/tests/mcast_ipv?_recv.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_FILEINFO_VERSION /{s/.* "//;s/".*$//;p}' ext/fileinfo/php_fileinfo.h)
if test "$ver" != "%{fileinfover}"; then
   : Error: Upstream FILEINFO version is now ${ver}, expecting %{fileinfover}.
   : Update the fileinfover macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_PHAR_VERSION /{s/.* "//;s/".*$//;p}' ext/phar/php_phar.h)
if test "$ver" != "%{pharver}"; then
   : Error: Upstream PHAR version is now ${ver}, expecting %{pharver}.
   : Update the pharver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_ZIP_VERSION /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the zipver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_ZENDOPCACHE_VERSION /{s/.* "//;s/".*$//;p}' ext/opcache/ZendAccelerator.h)
if test "$ver" != "%{opcachever}"; then
   : Error: Upstream OPcache version is now ${ver}, expecting %{opcachever}.
   : Update the opcachever macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

%if %{with_tmpfiles}
# php-fpm configuration files for tmpfiles.d
echo "d %{_localstatedir}/run/php-fpm 755 root root" >php-fpm.tmpfiles
%endif

# bring in newer config.guess and config.sub for aarch64 support
cp -f /usr/lib/rpm/config.{guess,sub} .

%build
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:
libtoolize --force --copy
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat `aclocal --print-ac-dir`/libtool.m4 > build/libtool.m4
%endif

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.7. Workaround:
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
%configure \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-exec-dir=%{_bindir} \
    --with-freetype-dir=%{_root_prefix} \
    --with-png-dir=%{_root_prefix} \
    --with-xpm-dir=%{_root_prefix} \
    --enable-gd-native-ttf \
    --with-t1lib=%{_root_prefix} \
    --without-gdbm \
    --with-jpeg-dir=%{_root_prefix} \
    --with-openssl \
    --with-pcre-regex \
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml-dir=%{_root_prefix} \
    --with-system-tzdata \
    --with-mhash \
%if %{with_dtrace}
    --enable-dtrace \
%endif
    $* 
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

with_shared="--with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_root_prefix} \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --with-interbase=shared,%{_libdir}/firebird \
      --with-pdo-firebird=shared,%{_libdir}/firebird \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_root_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_root_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_root_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_root_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_root_prefix} \
      --with-pdo-sqlite=shared,%{_root_prefix} \
      --with-pdo-dblib=shared,%{_root_prefix} \
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
      --with-sqlite3=shared,%{_root_prefix} \
%else
      --without-sqlite3 \
%endif
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%endif
%if %{with_libzip}
      --with-libzip \
%endif
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_root_prefix} \
      --with-tidy=shared,%{_root_prefix} \
      --with-mssql=shared,%{_root_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_root_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
      --with-icu-dir=%{_root_prefix} \
%else
%if 0%{?scl:1}
      --with-icu-config=%{_bindir}/icu-config
%else
      --with-icu-config=%{_root_bindir}/icu42-icu-config
%endif
%endif
      --with-enchant=shared,%{_root_prefix} \
      --with-recode=shared,%{_root_prefix} \
      --enable-opcache"

with_shared2="--enable-pdo=shared \
      --with-mysql=shared,%{_root_prefix} \
      --with-mysqli=shared,%{mysql_config} \
      --with-pdo-mysql=shared,%{mysql_config} \
      --without-pdo-sqlite"

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-xmlreader --disable-xmlwriter \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem \
      --disable-opcache"

# Build /usr/bin/php with the CLI SAPI, /usr/bin/php-cgi with the CGI SAPI,
# and all the shared extensions
pushd build-cli
build --enable-force-cgi-redirect \
      --disable-phpdbg \
      --libdir=%{_libdir}/php \
      --enable-pcntl \
      --enable-fastcgi \
      --without-readline \
      --with-libedit \
      ${with_shared}
popd

# Build Apache module
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php \
      ${with_shared2} ${without_shared}
popd

%if %{with_fpm}
# Build php-fpm
pushd build-fpm
build --enable-fpm \
%if %{with_systemd}
      --with-fpm-systemd \
%endif
      --libdir=%{_libdir}/php \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd
%endif

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd

%if %{with_zts}
# Build a special thread-safe cli (mainly for modules)
pushd build-ztscli
EXTENSION_DIR=%{_libdir}/php-zts/modules
build --enable-force-cgi-redirect \
      --disable-phpdbg \
      --enable-pcntl \
      --enable-fastcgi \
      --without-readline \
      --with-libedit \
      --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      ${with_shared}
popd

# Build a special thread-safe Apache SAPI
pushd build-zts
build --with-apxs2=%{_httpd_apxs} \
      --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      ${with_shared2} ${without_shared} \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d
popd
%endif

%if %{with_phpdbg}
# Build /usr/bin/phpdbg with readline support
pushd build-phpdbg
EXTENSION_DIR=%{_libdir}/php/modules
build --enable-phpdbg \
      --libdir=%{_libdir}/php \
      --with-readline \
      --without-libedit \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd
%endif

%check
%if %runselftest

# Increase stack size (required by bug54268.phpt)
ulimit -s 32712

cd build-apache
# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2 SKIP_ONLINE_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      cat "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_ SKIP_ONLINE_TESTS
%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%if %{with_zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# rename extensions build with mysqlnd
mv $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/mysqli.so \
   $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/pdo_mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/pdo_mysqlnd.so

%if %{with_libmysql}
# Install the extensions for the ZTS version modules for libmysql
make -C build-zts install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# rename ZTS binary
mv $RPM_BUILD_ROOT%{_bindir}/php        $RPM_BUILD_ROOT%{_bindir}/zts-php
mv $RPM_BUILD_ROOT%{_bindir}/phpize     $RPM_BUILD_ROOT%{_bindir}/zts-phpize
mv $RPM_BUILD_ROOT%{_bindir}/php-config $RPM_BUILD_ROOT%{_bindir}/zts-php-config
%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with_fpm}
# Install the php-fpm binary
make -C build-fpm install-fpm INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

%if %{with_phpdbg}
# Install the phpdbg binary
make -C build-phpdbg install-phpdbg INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install everything from the CLI/CGI SAPI build
make -C build-cli install INSTALL_ROOT=$RPM_BUILD_ROOT

# rename extensions build with mysqlnd
mv $RPM_BUILD_ROOT%{_libdir}/php/modules/mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{_libdir}/php/modules/mysqli.so \
   $RPM_BUILD_ROOT%{_libdir}/php/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{_libdir}/php/modules/pdo_mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php/modules/pdo_mysqlnd.so

%if %{with_libmysql}
# Install the mysql extension build with libmysql
make -C build-apache install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 php.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/php.gif

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/php/pear \
                  $RPM_BUILD_ROOT%{_datadir}/php

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_httpd_moddir}

%if %{with_zts}
# install the ZTS DSO
install -m 755 build-zts/libs/libphp5.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp5-zts.so
%endif

# Apache config fragment
%if %{?scl:1}0
install -m 755 -d $RPM_BUILD_ROOT%{_root_httpd_moddir}
ln -s %{_httpd_moddir}/libphp5.so      $RPM_BUILD_ROOT%{_root_httpd_moddir}/lib%{name}5.so
%endif
sed -e 's/libphp5/lib%{_name}5/' %{SOURCE9} >modconf
sed -e 's/libphp5/lib%{_name}5/' %{SOURCE10} >ztsmodconf
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# Single config file with httpd < 2.4 (fedora <= 17)
install -D -m 644 modconf $RPM_BUILD_ROOT%{_httpd_confdir}/%{_name}.conf
%if %{with_zts}
cat ztsmodconf >>$RPM_BUILD_ROOT%{_httpd_confdir}/%{_name}.conf
%endif
cat %{SOURCE1} >>$RPM_BUILD_ROOT%{_httpd_confdir}/%{_name}.conf
%else
# Dual config file with httpd >= 2.4 (fedora >= 18)
install -D -m 644 modconf $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-%{_name}.conf
%if %{with_zts}
cat ztsmodconf >>$RPM_BUILD_ROOT%{_httpd_modconfdir}/10-%{_name}.conf
%endif
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/%{_name}.conf
%endif
sed -e 's:/var/lib:%{_localstatedir}/lib:' \
    -i $RPM_BUILD_ROOT%{_httpd_confdir}/%{_name}.conf

sed -e 's:/var/lib:%{_localstatedir}/lib:' \
    -i $RPM_BUILD_ROOT%{_httpd_confdir}/%{_name}.conf

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%if %{with_zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/wsdlcache

%if %{with_fpm}
# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
sed -e 's:/var/run:%{_localstatedir}/run:' \
    -e 's:/var/log:%{_localstatedir}/log:' \
    -e 's:/etc:%{_sysconfdir}:' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
sed -e 's:/var/lib:%{_localstatedir}/lib:' \
    -e 's:/var/log:%{_localstatedir}/log:' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
%if %{with_tmpfiles}
# tmpfiles.d
install -m 755 -d $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 644 php-fpm.tmpfiles $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/php-fpm.conf
%endif
%if %{with_systemd}
sed -e "s/daemonise = yes/daemonise = no/" \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
# install systemd unit files and scripts for handling server startup
install -m 755 -d $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/%{?scl_prefix}php-fpm.service
sed -e 's:/run:%{_localstatedir}/run:' \
    -e 's:/etc:%{_sysconfdir}:' \
    -e 's:/usr/sbin:%{_sbindir}:' \
    -i $RPM_BUILD_ROOT%{_unitdir}/%{?scl_prefix}php-fpm.service
%else
# Service
install -m 755 -d $RPM_BUILD_ROOT%{_root_initddir}
install -m 755 %{SOURCE11} $RPM_BUILD_ROOT%{_root_initddir}/%{?scl_prefix}php-fpm
# Needed relocation for SCL
sed -e '/php-fpm.pid/s:/var:%{_localstatedir}:' \
    -e '/subsys/s/php-fpm/%{?scl_prefix}php-fpm/' \
    -e 's:/etc/sysconfig/php-fpm:%{_sysconfdir}/sysconfig/php-fpm:' \
    -e 's:/etc/php-fpm.conf:%{_sysconfdir}/php-fpm.conf:' \
    -e 's:/usr/sbin:%{_sbindir}:' \
    -i $RPM_BUILD_ROOT%{_root_initddir}/%{?scl_prefix}php-fpm
%endif
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_root_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_root_sysconfdir}/logrotate.d/%{?scl_prefix}php-fpm
sed -e 's:/run:%{_localstatedir}/run:' \
    -e 's:/var/log:%{_localstatedir}/log:' \
    -i $RPM_BUILD_ROOT%{_root_sysconfdir}/logrotate.d/%{?scl_prefix}php-fpm
# Environment file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php-fpm
%endif

# Fix the link
(cd $RPM_BUILD_ROOT%{_bindir}; ln -sfn phar.phar phar)

# make the cli commands available in standard root for SCL build
%if 0%{?scl:1}
#install -m 755 -d $RPM_BUILD_ROOT%{_root_bindir}
#ln -s %{_bindir}/php       $RPM_BUILD_ROOT%{_root_bindir}/%{?scl_prefix}php
#ln -s %{_bindir}/phar.phar $RPM_BUILD_ROOT%{_root_bindir}/%{?scl_prefix}phar
%endif

# Copy stub .ini file for opcache
install -m 644 %{SOURCE50} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache.ini
# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache-default.blacklist
sed -e 's:%{_root_sysconfdir}:%{_sysconfdir}:' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache.ini
%if %{with_zts}
install -m 644 $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache.ini $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/opcache.ini
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif


# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp xmlrpc imap \
    mysqlnd mysqlnd_mysql mysqlnd_mysqli pdo_mysqlnd \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    bz2 calendar ctype exif ftp gettext gmp iconv simplexml \
    sockets tokenizer \
    pdo pdo_pgsql pdo_odbc pdo_sqlite json %{zipmod} \
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
    sqlite3  \
%endif
%if %{with_libmysql}
    mysql mysqli pdo_mysql \
%endif
    interbase pdo_firebird \
    enchant phar fileinfo intl \
    mcrypt tidy pdo_dblib mssql pspell curl wddx \
    posix shmop sysvshm sysvsem sysvmsg recode xml; do

    # Make sure wddx is loaded after the xml extension, which it depends on
    if [ "$mod" = "wddx" ]
    then
        ini=xml_${mod}.ini
    else
        ini=${mod}.ini
    fi

    cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%if %{with_zts}
    cp $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} \
       $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini}
%endif
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${ini}
%if %{with_zts}
%attr(755,root,root) %{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php-zts.d/${ini}
%endif
EOF
done

mv files.xml files.xmlext

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
%if %{with_libmysql}
cat files.mysqli >> files.mysql
cat files.pdo_mysql >> files.mysql
%endif

# mysqlnd
cat files.mysqlnd_mysql \
    files.mysqlnd_mysqli \
    files.pdo_mysqlnd \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_dblib >> files.mssql
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
cat files.pdo_firebird >> files.interbase

# sysv* and posix in packaged in php-process
cat files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
cat files.sqlite3 >> files.pdo
%endif

# Package most extensions in -common.
cat files.json files.curl files.phar files.fileinfo \
    files.bz2 files.calendar files.ctype files.exif files.ftp files.gettext \
    files.gmp files.iconv files.simplexml files.shmop files.xmlext \
    files.sockets files.tokenizer > files.common
%if %{with_zip}
cat files.zip >> files.common
%endif

# Install the macros file:
install -d $RPM_BUILD_ROOT%{_macrosdir}
sed -e "s/@PHP_APIVER@/%{apiver}%{isasuffix}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}%{isasuffix}/" \
    -e "s/@PHP_PDOVER@/%{pdover}%{isasuffix}/" \
    -e "s/@PHP_VERSION@/%{version}/" \
%if 0%{?scl:1}
    -e "s/^\%/\%%{scl}_/" \
%endif
%if ! %{with_zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros.php
install -m 644 -c macros.php \
           $RPM_BUILD_ROOT%{_macrosdir}/macros.%{_name}

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm files.* macros.php

%if %{with_fpm}
%pre fpm
# Add the "apache" user as we don't require httpd
getent group  apache >/dev/null || \
  groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d %{_httpd_contentdir} -c "Apache" apache
exit 0

%if %{with_systemd}
%post fpm
%systemd_post %{?scl_prefix}php-fpm.service

%preun fpm
%systemd_preun %{?scl_prefix}php-fpm.service

%postun fpm
%systemd_postun_with_restart %{?scl_prefix}php-fpm.service

# Handle upgrading from SysV initscript to native systemd unit.
# We can tell if a SysV version of php-fpm was previously installed by
# checking to see if the initscript is present.
%triggerun fpm -- %{?scl_prefix}php-fpm
if [ -f /etc/rc.d/init.d/%{?scl_prefix}php-fpm ]; then
    # Save the current service runlevel info
    # User must manually run systemd-sysv-convert --apply %{?scl_prefix}php-fpm
    # to migrate them to systemd targets
    /usr/bin/systemd-sysv-convert --save %{?scl_prefix}php-fpm >/dev/null 2>&1 || :

    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del %{?scl_prefix}php-fpm >/dev/null 2>&1 || :
    /bin/systemctl try-restart %{?scl_prefix}php-fpm.service >/dev/null 2>&1 || :
fi

%else

%post fpm
/sbin/chkconfig --add %{?scl_prefix}php-fpm

%preun fpm
if [ "$1" = 0 ] ; then
    /sbin/service %{?scl_prefix}php-fpm stop >/dev/null 2>&1
    /sbin/chkconfig --del %{?scl_prefix}php-fpm
fi

%postun fpm
if [ "$1" -ge "1" ] ; then
service %{?scl_prefix}php-fpm condrestart &> /dev/null || :
fi

%endif

%endif

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig

%files
%{_httpd_moddir}/libphp5.so
%if %{with_zts}
%{_httpd_moddir}/libphp5-zts.so
%endif
%if 0%{?scl:1}
%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_root_httpd_moddir}/lib%{name}5.so
%endif
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%config(noreplace) %{_httpd_confdir}/%{_name}.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-%{_name}.conf
%endif
%{_httpd_contentdir}/icons/php.gif

%files common -f files.common
%doc CODING_STANDARDS CREDITS EXTENSIONS LICENSE NEWS README*
%doc Zend/ZEND_* TSRM_LICENSE regex_COPYRIGHT
%doc libmagic_LICENSE
%doc phar_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with_zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_localstatedir}/lib/php
%dir %{_libdir}/php/pear
%dir %{_datadir}/php

%files cli
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*
%doc sapi/cgi/README* sapi/cli/README
#{?scl: %{_root_bindir}/%{?scl_prefix}php}
#{?scl: %{_root_bindir}/%{?scl_prefix}phar}

%if %{with_phpdbg}
%files phpdbg
%{_bindir}/phpdbg
%{_mandir}/man1/phpdbg.1*
%endif

%if %{with_fpm}
%files fpm
%doc php-fpm.conf.default
%doc fpm_LICENSE
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_root_sysconfdir}/logrotate.d/%{?scl_prefix}php-fpm
%config(noreplace) %{_sysconfdir}/sysconfig/php-fpm

%if %{with_tmpfiles}
%{_prefix}/lib/tmpfiles.d/php-fpm.conf
%endif
%if %{with_systemd}
%{_unitdir}/%{?scl_prefix}php-fpm.service
%else
%{_root_initddir}/%{?scl_prefix}php-fpm
%endif

%{_sbindir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%dir %{_localstatedir}/run/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html
%endif

%files devel
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with_zts}
%{_bindir}/zts-php-config
%{_includedir}/php-zts
%{_bindir}/zts-phpize
# useful only to test other module during build
%{_bindir}/zts-php
%{_libdir}/php-zts/build
%endif
%{_mandir}/man1/php-config.1*
%{_macrosdir}/macros.%{_name}

%files embedded
%{_libdir}/libphp5.so
%{_libdir}/libphp5-%{embed_version}.so

%files opcache
%attr(755,root,root) %{_libdir}/php/modules/opcache.so
%config(noreplace) %{_sysconfdir}/php.d/opcache.ini
%config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with_zts}
%attr(755,root,root) %{_libdir}/php-zts/modules/opcache.so
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache.ini
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif

%files pgsql -f files.pgsql
%if %{with_libmysql}
%files mysql -f files.mysql
%endif
%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%doc libmbfl_LICENSE
%doc oniguruma_COPYING
%doc ucgendat_LICENSE
%files gd -f files.gd
%doc libgd_README
%doc libgd_COPYING
%files soap -f files.soap
%files bcmath -f files.bcmath
%doc libbcmath_COPYING
%files dba -f files.dba
%files pdo -f files.pdo
%files mcrypt -f files.mcrypt
%files tidy -f files.tidy
%files mssql -f files.mssql
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%files interbase -f files.interbase
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd

%changelog
* Fri May 18 2018 Andy Thompson <andy@webtatic.com> - 5.6.36-1
- update to php-5.6.36

* Fri Mar 30 2018 Andy Thompson <andy@webtatic.com> - 5.6.35-1
- update to php-5.6.35

* Fri Mar 02 2018 Andy Thompson <andy@webtatic.com> - 5.6.34-1
- update to php-5.6.34

* Sun Jan 14 2018 Andy Thompson <andy@webtatic.com> - 5.6.33-1
- update to php-5.6.33

* Sun Oct 29 2017 Andy Thompson <andy@webtatic.com> - 5.6.32-1
- update to php-5.6.32

* Thu Sep 14 2017 Andy Thompson <andy@webtatic.com> - 5.6.31-2
- rebuild for EL7.4

* Fri Jul 07 2017 Andy Thompson <andy@webtatic.com> - 5.6.31-1
- update to php-5.6.31

* Thu Jan 19 2017 Andy Thompson <andy@webtatic.com> - 5.6.30-1
- update to php-5.6.30

* Sat Dec 10 2016 Andy Thompson <andy@webtatic.com> - 5.6.29-1
- update to php-5.6.29

* Thu Nov 10 2016 Andy Thompson <andy@webtatic.com> - 5.6.28-1
- update to php-5.6.28

* Sat Oct 15 2016 Andy Thompson <andy@webtatic.com> - 5.6.27-1
- update to php-5.6.27

* Sat Sep 17 2016 Andy Thompson <andy@webtatic.com> - 5.6.26-1
- update to php-5.6.26

* Sat Aug 20 2016 Andy Thompson <andy@webtatic.com> - 5.6.25-1
- update to php-5.6.25

* Thu Jul 21 2016 Andy Thompson <andy@webtatic.com> - 5.6.24-1
- update to php-5.6.24

* Thu Jun 23 2016 Andy Thompson <andy@webtatic.com> - 5.6.23-1
- update to php-5.6.23
- update conflicts version to 5.6

* Sat May 28 2016 Andy Thompson <andy@webtatic.com> - 5.6.22-1
- update to php-5.6.22

* Sat Apr 30 2016 Andy Thompson <andy@webtatic.com> - 5.6.21-1
- update to php-5.6.21
- remove odbctimer patch for upstream fix

* Sat Apr 02 2016 Andy Thompson <andy@webtatic.com> - 5.6.20-1
- update to php-5.6.20

* Fri Mar 04 2016 Andy Thompson <andy@webtatic.com> - 5.6.19-1
- update to php-5.6.19

* Thu Feb 04 2016 Andy Thompson <andy@webtatic.com> - 5.6.18-1
- update to php-5.6.18

* Sun Jan 31 2016 Andy Thompson <andy@webtatic.com> - 5.6.17-2
- Add curltlsconst patch to introduce backported curl constants

* Sat Jan 09 2016 Andy Thompson <andy@webtatic.com> - 5.6.17-1
- update to php-5.6.17
- adapt libdb patch for upstream changes

* Fri Nov 27 2015 Andy Thompson <andy@webtatic.com> - 5.6.16-1
- update to php-5.6.16

* Sat Oct 31 2015 Andy Thompson <andy@webtatic.com> - 5.6.15-1
- update to php-5.6.15

* Sun Oct 11 2015 Andy Thompson <andy@webtatic.com> - 5.6.14-2
- Add php-fpm conditional restart on EL < 7
- Simplify spec conditionals

* Thu Oct 01 2015 Andy Thompson <andy@webtatic.com> - 5.6.14-1
- update to php-5.6.14

* Fri Sep 04 2015 Andy Thompson <andy@webtatic.com> - 5.6.13-1
- update to php-5.6.13
- adapt systzdata patch for upstream changes

* Sun Aug 09 2015 Andy Thompson <andy@webtatic.com> - 5.6.12-1
- update to php-5.6.12

* Fri Jul 10 2015 Andy Thompson <andy@webtatic.com> - 5.6.11-1
- update to php-5.6.11

* Thu Jun 11 2015 Andy Thompson <andy@webtatic.com> - 5.6.10-1
- update to php-5.6.10
- update opcachever to upstream latest version

* Fri May 15 2015 Andy Thompson <andy@webtatic.com> - 5.6.9-1
- update to php-5.6.9
- update systzdata patch to support latest upstream
- update zipver to reflect version in source

* Thu Apr 16 2015 Andy Thompson <andy@webtatic.com> - 5.6.8-1
- update to php-5.6.8

* Sat Mar 21 2015 Andy Thompson <andy@webtatic.com> - 5.6.7-1
- update to php-5.6.7

* Thu Feb 19 2015 Andy Thompson <andy@webtatic.com> - 5.6.6-1
- update to php-5.6.6

* Thu Jan 22 2015 Andy Thompson <andy@webtatic.com> - 5.6.5-1
- update to php-5.6.5

* Fri Dec 19 2014 Andy Thompson <andy@webtatic.com> - 5.6.4-1
- update to php-5.6.4

* Thu Nov 13 2014 Andy Thompson <andy@webtatic.com> - 5.6.3-1
- update to php-5.6.3

* Fri Oct 17 2014 Andy Thompson <andy@webtatic.com> - 5.6.2-1
- update to php-5.6.2

* Fri Oct 03 2014 Andy Thompson <andy@webtatic.com> - 5.6.1-1
- update to php-5.6.1

* Thu Oct 02 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-2
- Add tmpfiles.d config to recreate run directory

* Thu Aug 28 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-1
- update to php-5.6.0

* Fri Aug 15 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.11.RC4
- update to php-5.6.0RC4

* Fri Aug 01 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.10.RC3
- update to php-5.6.0RC2
- remove patch for upstream fix

* Fri Jul 04 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.9.RC2
- update to php-5.6.0RC2
- add patch for broken phpdbg man page install
- add phpdbg man page to phpdbg package

* Fri Jun 20 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.8.RC1
- update to php-5.6.0RC1

* Sat Jun 07 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.7.beta4
- update to php-5.6.0beta4

* Fri May 16 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.6.beta3
- update to php-5.6.0beta3
- remove patch for #67186 now fixed upstream

* Fri May 02 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.5.beta2
- update to php-5.6.0beta2
- add patch for mysqli build failure #67186

* Sun Apr 13 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.4.beta1
- update to php-5.6.0beta1

* Sat Mar 15 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.3.alpha3
- update to php-5.6.0alpha3
- remove patch for mysql build failure, now in upstream
- replace opcache version constant with new constant

* Sun Feb 16 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.2.alpha2
- update to php-5.6.0alpha2
- add patch for mysqli build failure
- update the php.ini to latest

* Sun Feb 02 2014 Andy Thompson <andy@webtatic.com> - 5.6.0-0.1.alpha1
- fork php55w package
- update to php-5.6.0alpha1
- add php56w-phpdbg package output
