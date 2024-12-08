DISABLE HYPER-V. TURN OFF DEVICE GUARD, CREDENTIAL GUARD, MEMORY ISOLATION. Otherwise, it'll run like crap without AMD-V (see vbox logs).
```
Control Panel -> Programs & Features -> Turn Windows Features on or off -> Hyper-V (possibly also Windows Hypervisor Platform, Windows Sub for Linux)
```

powershell (run as administrator)
```
> bcdedit /set hypervisorlaunchtype off
> Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-Hypervisor
> dism /online /disable-feature /featurename:microsoft-hyper-v-all
```

regedit
```
> Add dword32 Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\DeviceGuard\EnableVirtualizationBasedSecurity as 0
> Add dword32 Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\LsaCfgFlags as 0
> Change Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity to 0
```
