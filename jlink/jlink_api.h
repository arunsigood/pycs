#ifndef JLINK_API_H
#define JLINK_API_H
char *JLINKARM_GetCompileDateTime(void);
int JLINKARM_GetDLLVersion(void);
int JLINK_GetDLLVersion(void); // calls JLINKARM_GetDLLVersion
// JLINK_AddMirrorArea
// JLINK_AddMirrorAreaEx
// JLINKARM_AddMirrorArea
// JLINKARM_AddMirrorAreaEx
// JLINKARM_BeginDownload
// JLINKARM_BMI_Get
// JLINKARM_BMI_Set
// JLINKARM_CDC_Read
// JLINKARM_CDC_SetBaudrate
// JLINKARM_CDC_SetHookFuncs
// JLINKARM_CDC_SetRTSState
// JLINKARM_CDC_SetTimeoutLastCDCRead
// JLINKARM_CDC_Write
// JLINKARM_Clock
// JLINKARM_Close
// JLINKARM_ClrBP
// JLINKARM_ClrBPEx
// JLINKARM_ClrDataEvent
// JLINKARM_ClrError
// JLINKARM_ClrExecTime
// JLINKARM_ClrRESET
// JLINKARM_ClrTCK
// JLINKARM_ClrTDI
// JLINKARM_ClrTMS
// JLINKARM_ClrTRST
// JLINKARM_ClrWP
// JLINKARM_Communicate
// JLINKARM_CommunicateEx
// JLINKARM_ConfigJTAG
// JLINKARM_Connect
// JLINKARM_Core2CoreName
// JLINKARM_CORE_GetFound
// JLINKARM_CORE_Select
// JLINKARM_CORESIGHT_Configure
// JLINKARM_CORESIGHT_ReadAPDPReg
// JLINKARM_CORESIGHT_WriteAPDPReg
// JLINKARM_CP15_IsPresent
// JLINKARM_CP15_ReadEx
// JLINKARM_CP15_ReadReg
// JLINKARM_CP15_WriteEx
// JLINKARM_CP15_WriteReg
// JLINKARM_DEVICE_GetIndex
// JLINKARM_DEVICE_GetInfo
// JLINKARM_DEVICE_SelectDialog
// JLINKARM_DisassembleInst
// JLINKARM_DisassembleInstEx
// JLINKARM_DownloadECode
// JLINKARM_EMU_COM_IsSupported
// JLINKARM_EMU_COM_Read
// JLINKARM_EMU_COM_Write
// JLINKARM_EMU_FILE_Delete
// JLINKARM_EMU_FILE_GetList
// JLINKARM_EMU_FILE_GetSize
// JLINKARM_EMU_FILE_Read
// JLINKARM_EMU_FILE_Write
// JLINKARM_EMU_GetCounters
// JLINKARM_EMU_GetDeviceInfo
// JLINKARM_EMU_GetList
// JLINKARM_EMU_GetMaxMemBlock
// JLINKARM_EMU_GetNumConnections
// JLINKARM_EMU_GetNumDevices
// JLINKARM_EMU_GetProductId
// JLINKARM_EMU_GetProductName
// JLINKARM_EMU_HasCapEx
// JLINKARM_EMU_HasCPUCap
// JLINKARM_EMU_IsConnected
// JLINKARM_EMU_SelectByIndex
// JLINKARM_EMU_SelectByUSBSN
// JLINKARM_EMU_SelectIP
// JLINKARM_EMU_SelectIPBySN
// JLINKARM_EMU_TestNRSpeed
// JLINKARM_EMU_TestNWSpeed
// JLINKARM_EnableCheckModeAfterWrite
// JLINKARM_EnableFlashCache
// JLINKARM_EnableLog
// JLINKARM_EnableLogCom
// JLINKARM_EnablePerformanceCnt
// JLINKARM_EnableSoftBPs
// JLINKARM_EndDownload
// JLINKARM_ETB_IsPresent
// JLINKARM_ETB_ReadReg
// JLINKARM_ETB_WriteReg
// JLINKARM_ETM_IsPresent
// JLINKARM_ETM_ReadReg
// JLINKARM_ETM_StartTrace
// JLINKARM_ETM_WriteReg
// JLINKARM_ExecCommand
// JLINKARM_ExecECode
// JLINKARM_FindBP
// JLINKARM_FreeMem
// JLINKARM_GetBPInfo
// JLINKARM_GetBPInfoEx
// JLINKARM_GetConfigData
// JLINKARM_GetDebugInfo
// JLINKARM_GetDeviceFamily
// JLINKARM_GetDeviceId
// JLINKARM_GetEmbeddedFWString
// JLINKARM_GetEmbeddedFWVersion
// JLINKARM_GetEmuCaps
// JLINKARM_GetEmuCapsEx
// JLINKARM_GetExecTime
// JLINKARM_GetFeatureString
// JLINKARM_GetFirmwareString
// JLINKARM_GetHardwareVersion
// JLINKARM_GetHWInfo
// JLINKARM_GetHWStatus
// JLINKARM_GetId
// JLINKARM_GetIdData
// JLINKARM_GetIRLen
// JLINKARM_GetMOEs
// JLINKARM_GetNumBPs
// JLINKARM_GetNumBPUnits
// JLINKARM_GetNumWPs
// JLINKARM_GetNumWPUnits
// JLINKARM_GetOEMString
// JLINKARM_GetPerformanceCnt
// JLINKARM_GetpSharedMem
// JLINKARM_GetRegisterList
// JLINKARM_GetRegisterName
// JLINKARM_GetResetTypeDesc
// JLINKARM_GetScanLen
// JLINKARM_GetSelDevice
// JLINKARM_GetSN
// JLINKARM_GetSpeed
// JLINKARM_GetSpeedInfo
// JLINKARM_GetU32
// JLINKARM_GetWPInfoEx
// JLINKARM_Go
// JLINKARM_GoAllowSim
// JLINKARM_GoEx
// JLINKARM_GoHalt
// JLINKARM_GoIntDis
// JLINKARM_Halt
// JLINKARM_HasError
// JLINKARM_INDICATORS_SetState
// JLINKARM_IsConnected
// JLINKARM_IsHalted
// JLINKARM_IsOpen
// JLINKARM_JTAG_ConfigDevices
// JLINKARM_JTAG_DisableIF
// JLINKARM_JTAG_EnableIF
// JLINKARM_JTAG_GetData
// JLINKARM_JTAG_GetDeviceId
// JLINKARM_JTAG_GetDeviceInfo
// JLINKARM_JTAG_GetU16
// JLINKARM_JTAG_GetU32
// JLINKARM_JTAG_GetU8
// JLINKARM_JTAG_StoreData
// JLINKARM_JTAG_StoreGetData
// JLINKARM_JTAG_StoreGetRaw
// JLINKARM_JTAG_StoreInst
// JLINKARM_JTAG_StoreRaw
// JLINKARM_JTAG_SyncBits
// JLINKARM_JTAG_SyncBytes
// JLINKARM_JTAG_WriteData
// JLINKARM_Lock
// JLINKARM_MeasureCPUSpeed
// JLINKARM_MeasureCPUSpeedEx
// JLINKARM_MeasureRTCKReactTime
// JLINKARM_MeasureSCLen
// JLINKARM_NET_Close
// JLINKARM_NET_Open
// JLINKARM_Open
// JLINKARM_OpenEx
// JLINKARM_PCODE_Assemble
// JLINKARM_PCODE_Exec
// JLINKARM_PCODE_GetCaps
// JLINKARM_PCODE_GetDebugAPI
// JLINKARM_PCODE_GetS32Version
// JLINKARM_PERIODIC_ConfReadMem
// JLINKARM_PERIODIC_Control
// JLINKARM_PERIODIC_Read
// JLINKARM_RAWTRACE_Control
// JLINKARM_RAWTRACE_Read
// JLINKARM_ReadCodeMem
// JLINKARM_ReadConfigReg
// JLINKARM_ReadControlReg
// JLINKARM_ReadDCC
// JLINKARM_ReadDCCFast
// JLINKARM_ReadDebugPort
// JLINKARM_ReadDebugReg
// JLINKARM_ReadEmu
// JLINKARM_ReadEmuConfigMem
// JLINKARM_ReadICEReg
// JLINKARM_ReadMem
// JLINKARM_ReadMemEx
// JLINKARM_ReadMemHW
// JLINKARM_ReadMemIndirect
// JLINKARM_ReadMemU16
// JLINKARM_ReadMemU32
// JLINKARM_ReadMemU64
// JLINKARM_ReadMemU8
// JLINKARM_ReadReg
// JLINKARM_ReadRegs
// JLINKARM_ReadTerminal
// JLINKARM_Reset
// JLINKARM_ResetNoHalt
// JLINKARM_ResetPullsRESET
// JLINKARM_ResetPullsTRST
// JLINKARM_ResetTRST
// JLINKARM_SelDevice
// JLINKARM_SelectDeviceFamily
// JLINKARM_SelectIP
// JLINKARM_SelectTraceSource
// JLINKARM_SelectUSB
// JLINKARM_SetBP
// JLINKARM_SetBPEx
// JLINKARM_SetCoreIndex
// JLINKARM_SetDataEvent
// JLINKARM_SetDebugUnitBlockMask
// JLINKARM_SetEndian
// JLINKARM_SetErrorOutHandler
// JLINKARM_SetFlashArea
// JLINKARM_SetInitRegsOnReset
// JLINKARM_SetLogFile
// JLINKARM_SetMaxSpeed
// JLINKARM_SetRESET
// JLINKARM_SetResetDelay
// JLINKARM_SetResetPara
// JLINKARM_SetResetType
// JLINKARM_SetSpeed
// JLINKARM_SetTCK
// JLINKARM_SetTDI
// JLINKARM_SetTMS
// JLINKARM_SetTRST
// JLINKARM_SetWaitFunction
// JLINKARM_SetWarnOutHandler
// JLINKARM_SetWP
// JLINKARM_SimulateInstruction
// JLINKARM_Step
// JLINKARM_StepComposite
// JLINKARM_StoreBits
// JLINKARM_StoreCmd
// JLINKARM_StoreData
// JLINKARM_SWD_DisableSWCLK
// JLINKARM_SWD_EnableSWCLK
// JLINKARM_SWD_SetDirIn
// JLINKARM_SWD_SetDirOut
// JLINKARM_SWO_Control
// JLINKARM_SWO_DisableTarget
// JLINKARM_SWO_EnableTarget
// JLINKARM_SWO_GetCompatibleSpeeds
// JLINKARM_SWO_Read
// JLINKARM_SWO_ReadStimulus
// JLINKARM_Test
// JLINKARM_TIF_GetAvailable
// JLINKARM_TIF_Select
// JLINKARM_TRACE_AddInst
// JLINKARM_TRACE_AddItems
// JLINKARM_TRACE_Control
// JLINKARM_TRACE_Read
// JLINKARM_Unlock
// JLINKARM_UpdateFirmware
// JLINKARM_UpdateFirmwareIfNewer
// JLINKARM_UpdateReplaceFirmware
// JLINKARM_WA_AddRange
// JLINKARM_WaitDCCRead
// JLINKARM_WaitForHalt
// JLINKARM_WA_Restore
// JLINKARM_WriteBits
// JLINKARM_WriteConfigReg
// JLINKARM_WriteControlReg
// JLINKARM_WriteDCC
// JLINKARM_WriteDCCFast
// JLINKARM_WriteDebugPort
// JLINKARM_WriteDebugReg
// JLINKARM_WriteEmu
// JLINKARM_WriteEmuConfigMem
// JLINKARM_WriteICEReg
// JLINKARM_WriteMem
// JLINKARM_WriteMemDelayed
// JLINKARM_WriteMemEx
// JLINKARM_WriteMemHW
// JLINKARM_WriteMemMultiple
// JLINKARM_WriteReg
// JLINKARM_WriteRegs
// JLINKARM_WriteU16
// JLINKARM_WriteU32
// JLINKARM_WriteU64
// JLINKARM_WriteU8
// JLINKARM_WriteVectorCatch
// JLINKARM_WriteVerifyMem
// JLINK_BeginDownload
// JLINK_Clock
// JLINK_Close
// JLINK_ClrBP
// JLINK_ClrBPEx
// JLINK_ClrDataEvent
// JLINK_ClrError
// JLINK_ClrExecTime
// JLINK_ClrRESET
// JLINK_ClrTCK
// JLINK_ClrTDI
// JLINK_ClrTMS
// JLINK_ClrTRST
// JLINK_ClrWP
// JLINK_Communicate
// JLINK_ConfigJTAG
// JLINK_Configure
// JLINK_Connect
// JLINK_CORE_GetFound
// JLINK_CORE_Select
// JLINK_CORESIGHT_Configure
// JLINK_CORESIGHT_ReadAPDPReg
// JLINK_CORESIGHT_WriteAPDPReg
// JLINK_CP15_IsPresent
// JLINK_CP15_ReadEx
// JLINK_CP15_ReadReg
// JLINK_CP15_WriteEx
// JLINK_CP15_WriteReg
// JLINK_DEVICE_GetInfo
// JLINK_DIALOG_Configure
// JLINK_DIALOG_ConfigureEx
// JLINK_DownloadECode
// JLINK_DownloadFile
// JLINK_EMU_AddLicense
// JLINK_EMU_COM_IsSupported
// JLINK_EMU_COM_Read
// JLINK_EMU_COM_Write
// JLINK_EMU_EraseLicenses
// JLINK_EMU_FILE_Delete
// JLINK_EMU_FILE_GetList
// JLINK_EMU_FILE_GetSize
// JLINK_EMU_FILE_Read
// JLINK_EMU_FILE_Write
// JLINK_EMU_GetCounters
// JLINK_EMU_GetDeviceInfo
// JLINK_EMU_GetLicenses
// JLINK_EMU_GetList
// JLINK_EMU_GetMaxMemBlock
// JLINK_EMU_GetNumConnections
// JLINK_EMU_GetNumDevices
// JLINK_EMU_GetProductId
// JLINK_EMU_GetProductName
// JLINK_EMU_GPIO_GetProps
// JLINK_EMU_GPIO_GetState
// JLINK_EMU_GPIO_SetState
// JLINK_EMU_HasCapEx
// JLINK_EMU_HasCPUCap
// JLINK_EMU_IsConnected
// JLINK_EMU_SelectByIndex
// JLINK_EMU_SelectByUSBSN
// JLINK_EMU_SelectIP
// JLINK_EMU_SelectIPBySN
// JLINK_EMU_TestNRSpeed
// JLINK_EMU_TestNWSpeed
// JLINK_EnableCheckModeAfterWrite
// JLINK_EnableFlashCache
// JLINK_EnableLog
// JLINK_EnableLogCom
// JLINK_EnablePerformanceCnt
// JLINK_EnableSoftBPs
// JLINK_EndDownload
// JLINK_EraseChip
// JLINK_ETB_IsPresent
// JLINK_ETB_ReadReg
// JLINK_ETB_WriteReg
// JLINK_ETM_IsPresent
// JLINK_ETM_ReadReg
// JLINK_ETM_StartTrace
// JLINK_ETM_WriteReg
// JLINK_ExecCommand
// JLINK_ExecECode
// JLINK_FindBP
// JLINK_GetAvailableLicense
// JLINK_GetBPInfoEx
// JLINK_GetCompileDateTime
// JLINK_GetConfigData
// JLINK_GetDebugInfo
// JLINK_GetDeviceFamily
// JLINK_GetEmbeddedFWString
// JLINK_GetEmbeddedFWVersion
// JLINK_GetEmuCaps
// JLINK_GetEmuCapsEx
// JLINK_GetExecTime
// JLINK_GetFeatureString
// JLINK_GetFirmwareString
// JLINK_GetHardwareVersion
// JLINK_GetHWInfo
// JLINK_GetHWStatus
// JLINK_GetId
// JLINK_GetIdData
// JLINK_GetIRLen
// JLINK_GetMemZones
// JLINK_GetMOEs
// JLINK_GetNumBPs
// JLINK_GetNumBPUnits
// JLINK_GetNumWPs
// JLINK_GetNumWPUnits
// JLINK_GetOEMString
// JLINK_GetPCode
// JLINK_GetPerformanceCnt
// JLINK_GetpFunc
// JLINK_GetpSharedMem
// JLINK_GetRegisterList
// JLINK_GetRegisterName
// JLINK_GetResetTypeDesc
// JLINK_GetScanLen
// JLINK_GetSelDevice
// JLINK_GetSN
// JLINK_GetSpeed
// JLINK_GetSpeedInfo
// JLINK_GetU32
// JLINK_GetWPInfoEx
// JLINK_Go
// JLINK_GoAllowSim
// JLINK_GoEx
// JLINK_GoHalt
// JLINK_GoIntDis
// JLINK_Halt
// JLINK_HasError
// JLINK_HSS_GetCaps
// JLINK_HSS_Read
// JLINK_HSS_Start
// JLINK_HSS_Stop
// JLINK_INDICATORS_SetState
// JLINK_IsConnected
// JLINK_IsHalted
// JLINK_IsOpen
// JLINK_JTAG_ConfigDevices
// JLINK_JTAG_DisableIF
// JLINK_JTAG_EnableIF
// JLINK_JTAG_GetData
// JLINK_JTAG_GetDeviceId
// JLINK_JTAG_GetDeviceInfo
// JLINK_JTAG_GetU16
// JLINK_JTAG_GetU32
// JLINK_JTAG_GetU8
// JLINK_JTAG_StoreData
// JLINK_JTAG_StoreGetData
// JLINK_JTAG_StoreGetRaw
// JLINK_JTAG_StoreInst
// JLINK_JTAG_StoreRaw
// JLINK_JTAG_SyncBits
// JLINK_JTAG_SyncBytes
// JLINK_JTAG_WriteData
// JLINK_Lock
// JLINK_MeasureCPUSpeed
// JLINK_MeasureCPUSpeedEx
// JLINK_MeasureRTCKReactTime
// JLINK_MeasureSCLen
// JLINK_NET_Close
// JLINK_NET_Open
// JLINK_Open
// JLINK_OpenEx
// JLINK_PCODE_Exec
// JLINK_PCODE_GetCaps
// JLINK_PCODE_GetS32Version
// JLINK_POWERTRACE_Control
// JLINK_POWERTRACE_Read
// JLINK_PrintConfig
// JLINK_RAWTRACE_Control
// JLINK_RAWTRACE_Read
// JLINK_ReadCodeMem
// JLINK_ReadConfigReg
// JLINK_ReadControlReg
// JLINK_ReadDCC
// JLINK_ReadDCCFast
// JLINK_ReadDebugPort
// JLINK_ReadDebugReg
// JLINK_ReadEmu
// JLINK_ReadEmuConfigMem
// JLINK_ReadICEReg
// JLINK_ReadMem
// JLINK_ReadMemEx
// JLINK_ReadMemHW
// JLINK_ReadMemIndirect
// JLINK_ReadMemU16
// JLINK_ReadMemU32
// JLINK_ReadMemU64
// JLINK_ReadMemU8
// JLINK_ReadMemZonedEx
// JLINK_ReadReg
// JLINK_ReadRegs
// JLINK_ReadTerminal
// JLINK_Reset
// JLINK_ResetNoHalt
// JLINK_ResetPullsRESET
// JLINK_ResetPullsTRST
// JLINK_ResetTRST
// JLINK_RTTERMINAL_Control
// JLINK_RTTERMINAL_Read
// JLINK_RTTERMINAL_Write
// JLINK_SelDevice
// JLINK_SelectDeviceFamily
// JLINK_SelectIP
// JLINK_SelectTraceSource
// JLINK_SelectUSB
// JLINK_SetBP
// JLINK_SetBPEx
// JLINK_SetDataEvent
// JLINK_SetDebugUnitBlockMask
// JLINK_SetEndian
// JLINK_SetErrorOutHandler
// JLINK_SetFlashArea
// JLINK_SetFlashProgProgressCallback
// JLINK_SetHookUnsecureDialog
// JLINK_SetInitRegsOnReset
// JLINK_SetLogFile
// JLINK_SetMaxSpeed
// JLINK_SetRESET
// JLINK_SetResetDelay
// JLINK_SetResetPara
// JLINK_SetResetType
// JLINK_SetSpeed
// JLINK_SetTCK
// JLINK_SetTDI
// JLINK_SetTMS
// JLINK_SetTRST
// JLINK_SetWaitFunction
// JLINK_SetWarnOutHandler
// JLINK_SetWP
// JLINK_SimulateInstruction
// JLINK_SPI_Transfer
// JLINK_Step
// JLINK_StepComposite
// JLINK_StoreBits
// JLINK_StoreCmd
// JLINK_STRACE_Config
// JLINK_STRACE_Control
// JLINK_STRACE_Read
// JLINK_STRACE_Start
// JLINK_STRACE_Stop
// JLINK_SWD_DisableSWCLK
// JLINK_SWD_EnableSWCLK
// JLINK_SWD_GetData
// JLINK_SWD_GetU16
// JLINK_SWD_GetU32
// JLINK_SWD_GetU8
// JLINK_SWD_SetDirIn
// JLINK_SWD_SetDirOut
// JLINK_SWD_StoreGetRaw
// JLINK_SWD_StoreRaw
// JLINK_SWD_SyncBits
// JLINK_SWD_SyncBytes
// JLINK_SWO_Control
// JLINK_SWO_Read
// JLINK_Test
// JLINK_TIF_GetAvailable
// JLINK_TIF_Select
// JLINK_TRACE_AddInst
// JLINK_TRACE_AddItems
// JLINK_TRACE_Control
// JLINK_TRACE_Read
// JLINK_Unlock
// JLINK_UpdateFirmware
// JLINK_UpdateFirmwareIfNewer
// JLINK_UpdateReplaceFirmware
// JLINK_WA_AddRange
// JLINK_WaitDCCRead
// JLINK_WaitForHalt
// JLINK_WA_Restore
// JLINK_WriteBits
// JLINK_WriteConfigReg
// JLINK_WriteControlReg
// JLINK_WriteDCC
// JLINK_WriteDCCFast
// JLINK_WriteDebugPort
// JLINK_WriteDebugReg
// JLINK_WriteEmu
// JLINK_WriteEmuConfigMem
// JLINK_WriteICEReg
// JLINK_WriteMem
// JLINK_WriteMemDelayed
// JLINK_WriteMemEx
// JLINK_WriteMemHW
// JLINK_WriteMemZonedEx
// JLINK_WriteReg
// JLINK_WriteRegs
// JLINK_WriteU16
// JLINK_WriteU32
// JLINK_WriteU64
// JLINK_WriteU8
// JLINK_WriteVectorCatch
// JLINK_WriteVerifyMem
#endif // JLINK_API_H