# -*- coding: utf-8 -*-
# Code by Madhouse
import gettext
from os import path, chmod, makedirs
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from enigma import getDesktop

plugin_path = "/usr/lib/enigma2/python/Plugins/Extensions/Wireguard/speedtest.py"
cmd = f"python {plugin_path} --no-pre-allocate --share --secure"
png_tmp = "/tmp/speedtest.png"
headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
	"Accept-Encoding": "none",
	"Accept-Language": "en-US,en;q=0.8",
	"Connection": "keep-alive"
}

if path.exists(plugin_path):
	chmod(plugin_path, 0o755)

PluginLanguageDomain = "Wireguard"
PluginLanguagePath = "Extensions/Wireguard/locale"

ProviderList = "Surfshark, NordVpn, ProtonVpn, MullvadVpn, IVpn, oVpn.com"

PrivateKey = "/etc/PrivateKey.key"
PrivateKeyHdd = "/media/hdd/WgConfig/PrivateKey.key"
PrivateKeyUsb = "/media/usb/WgConfig/PrivateKey.key"

PathBypassHdd = "/media/hdd/WgConfig/WireguardBypass.txt"
PathBypassUsb = "/media/usb/WgConfig/WireguardBypass.txt"
PathBypass = "/etc/WgConfig/WireguardBypass.txt"

Token = "/etc/wg_token.key"

logo_wireguard = "/usr/lib/enigma2/python/Plugins/Extensions/Wireguard/skin/fhd/icons/logo_wireguard.png"

FileBypass = "WireguardBypass.txt"

WgShow = "wg show"

Version = "14.7"

StbModel = "Box"
hostname_path = "/etc/hostname"
if path.exists(hostname_path):
	with open(hostname_path, "r") as Model:
		Models = Model.read().strip()
		StbModel = Models.capitalize()

SKIN_PATH = "/usr/lib/enigma2/python/Plugins/Extensions/Wireguard/skin"
HD = getDesktop(0).size()

Directory = "/usr/lib/enigma2/python/Plugins/Extensions/Wireguard/ConfigFile"

required_directories = [
	"/etc/wireguard",
	"/media/hdd/WgConfig",
	"/media/usb/WgConfig",
	"/etc/WgConfig"
]

required_files = [
	PathBypassHdd,
	PrivateKeyHdd,
	PathBypassUsb,
	PrivateKeyUsb,
	PathBypass,
	PrivateKey,
	Token
]

def check_mount(mount_point):
	with open("/proc/mounts", "r") as f:
		for line in f:
			parts = line.split()
			if len(parts) > 1 and parts[1] == mount_point:
				return True
	return False

for directory in required_directories:
	if "/media/hdd" in directory and not check_mount("/media/hdd"):
		continue
	elif "/media/usb" in directory and not check_mount("/media/usb"):
		continue

	makedirs(directory, exist_ok=True)

for file in required_files:
	dir_path = path.dirname(file)

	if "/media/hdd" in dir_path and not check_mount("/media/hdd"):
		continue
	elif "/media/usb" in dir_path and not check_mount("/media/usb"):
		continue

	if path.exists(dir_path):
		if not path.exists(file):
			with open(file, "w") as f:
				f.write("")

for script in ["/etc/init.d/wireguard", "/etc/init.d/ipv6_disable"]:
	if path.exists(script):
		chmod(script, 0o755)

def localeInit():
	gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))

def _(txt):
	t = gettext.dgettext(PluginLanguageDomain, txt)
	if t == txt:
		t = gettext.dgettext("enigma2", txt)
	return t

def ngettext(singular, plural, n):
	t = gettext.dngettext("Wireguard", singular, plural, n)
	if t in (singular, plural):
		t = gettext.ngettext(singular, plural, n)
	return t

localeInit()
language.addCallback(localeInit)
