DISABLE HYPER-V. TURN OFF DEVICE GUARD, CREDENTIAL GUARD, MEMORY ISOLATION. Otherwise, it'll run like crap without AMD-V (see vbox logs).
```
Control Panel -> Programs & Features -> Turn Windows Features on or off -> Turn off
- Hyper-V 
- Windows Hypervisor Platform
- Windows Sub for Linux
- Virtual Machine Platform
```

```
Windows Security > Device security > Core isolation details > Memory integrity
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

Tools by Microsoft:

[DG_Readlness](https://www.microsoft.com/en-us/download/details.aspx?id=53337) will disable disable Device Guard or Credential Guard. There are two steps after reboot
- **Optional**: "Disable Credential Guard", to keep this option. **Do not** press "F3"
- **Required**: "Disable Virtualization Based Security", press "F3" to continus 

```
> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
> .\DG_Readiness_Tool_v3.6.ps1 -Disable
```
