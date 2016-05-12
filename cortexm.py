# -----------------------------------------------------------------------------
"""

Cortex-M CPU Operations

"""
# -----------------------------------------------------------------------------

import random
import time

import util
import io
import jlink
from regs import fld, fld_set, reg32, reg16, reg8, regset, memio

# -----------------------------------------------------------------------------

_help_memdisplay = (
    ('<adr> [len]', 'address (hex)'),
    ('', 'length (hex) - default is 0x40'),
)

_help_mem2file = (
    ('<adr> <len> [file]', 'address (hex)'),
    ('', 'length (hex)'),
    ('', 'filename - default is \"mem.bin\"'),
)

_help_file2mem = (
    ('<adr> [file] [len]', 'address (hex)'),
    ('', 'filename - default is \"mem.bin\"'),
    ('', 'length (hex) - default is file length'),
)

_help_memrd = (
    ('<adr>', 'address (hex)'),
)

_help_memwr = (
    ('<adr> <val>', 'address (hex)'),
    ('', 'value (hex)'),
)

_help_disassemble = (
    ('[adr] [len]', 'address (hex) - default is current pc'),
    ('', 'length (hex) - default is 0x10'),
)

_help_enable_disable = (
    ('<cr>', 'show current state'),
    ('[0/1]', 'disable or enable'),
)

# -----------------------------------------------------------------------------

_reg_names = (
  ('r0', jlink.REG_R0),
  ('r1', jlink.REG_R1),
  ('r2', jlink.REG_R2),
  ('r3', jlink.REG_R3),
  ('r4', jlink.REG_R4),
  ('r5', jlink.REG_R5),
  ('r6', jlink.REG_R6),
  ('r7', jlink.REG_R7),
  ('r8', jlink.REG_R8_USR),
  ('r9', jlink.REG_R9_USR),
  ('r10', jlink.REG_R10_USR),
  ('r11', jlink.REG_R11_USR),
  ('r12', jlink.REG_R12_USR),
  ('sp(r13)', jlink.REG_R13_USR),
  ('lr(r14)', jlink.REG_R14_USR),
  ('pc(r15)', jlink.REG_R15_PC),
  ('cpsr', jlink.REG_CPSR),
)

# -----------------------------------------------------------------------------
# Memory mapping of Cortex-Mx Hardware

SCS_BASE        = 0xE000E000 # System Control Space Base Address
ITM_BASE        = 0xE0000000 # ITM Base Address
DWT_BASE        = 0xE0001000 # DWT Base Address
TPI_BASE        = 0xE0040000 # TPI Base Address
CoreDebug_BASE  = 0xE000EDF0 # Core Debug Base Address
SysTick_BASE    = (SCS_BASE + 0x0010) # SysTick Base Address
NVIC_BASE       = (SCS_BASE + 0x0100) # NVIC Base Address
SCB_BASE        = (SCS_BASE + 0x0D00) # System Control Block Base Address
MPU_BASE        = (SCS_BASE + 0x0D90) # Memory Protection Unit Base Address
FPU_BASE        = (SCS_BASE + 0x0F30) # Floating Point Unit Base Address

# -----------------------------------------------------------------------------
# SysTick

def CLKSOURCE_format(x):
  return '(%d) %s' % (x, ('cpuclk', 'extclk')[x == 0])

f = []
f.append(fld('COUNTFLAG', 16, 16))
f.append(fld('CLKSOURCE', 2, 2, CLKSOURCE_format))
f.append(fld('TICKINT', 1, 1))
f.append(fld('ENABLE', 0, 0))
SysTick_CTRL_fields = fld_set('SysTick_CTRL', f)

def TENMS_format(x):
  return ('0', '(0x%06x) %.2f MHz' % (x, float(x)/1e+4))[x != 0]

f = []
f.append(fld('NOREF', 31, 31))
f.append(fld('SKEW', 30, 30))
f.append(fld('TENMS', 23, 0, TENMS_format))
SysTick_CALIB_fields = fld_set('SysTick_CALIB', f)

r = []
r.append(reg32('CTRL', 0x00, SysTick_CTRL_fields)) # (R/W) SysTick Control and Status Register
r.append(reg32('LOAD', 0x04)) # (R/W) SysTick Reload Value Register
r.append(reg32('VAL', 0x08)) # (R/W) SysTick Current Value Register
r.append(reg32('CALIB', 0x0c, SysTick_CALIB_fields)) # (R/ ) SysTick Calibration Register
systick_mX_regs = regset('SysTick', r)

# systick is a 24-bit down counter
SysTick_MAXCOUNT = (1 << 24) - 1

systick_regs = {
  'cortex-m4': (systick_mX_regs, SysTick_BASE),
  'cortex-m0+': (systick_mX_regs, SysTick_BASE),
}

# -----------------------------------------------------------------------------
# System Control Block

def Implementor_format(x):
  names = {
    0x41: 'ARM',
  }
  return '(0x%02x) %s' % (x, names.get(x, '?'))

def Part_Number_format(x):
  names = {
    0xc60: 'cortex-m0+',
    0xc20: 'cortex-m0',
    0xc21: 'cortex-m1',
    0xc23: 'cortex-m3',
    0xc24: 'cortex-m4',
    0xc27: 'cortex-m7',
  }
  return '(0x%03x) %s' % (x, names.get(x, '?'))

f = []
f.append(fld('Implementor', 31, 24, Implementor_format))
f.append(fld('Variant', 23, 20))
f.append(fld('Architecture', 19, 16))
f.append(fld('Part Number', 15, 4, Part_Number_format))
f.append(fld('Revision', 3, 0))
CPUID_fields = fld_set('CPUID', f)

r = []
r.append(reg32('CPUID', 0x000, CPUID_fields)) # (R/ ) CPUID Base Register
r.append(reg32('ICSR', 0x004)) # (R/W) Interrupt Control and State Register
r.append(reg32('VTOR', 0x008)) # (R/W) Vector Table Offset Register
r.append(reg32('AIRCR', 0x00C)) # (R/W) Application Interrupt and Reset Control Register
r.append(reg32('SCR', 0x010)) # (R/W) System Control Register
r.append(reg32('CCR', 0x014)) # (R/W) Configuration Control Register
r.append(reg8('SHPR', 0x018, None)) # base register for access
r.append(reg32('SHPR1', 0x018)) # (R/W) System Handlers Priority Registers
r.append(reg32('SHPR2', 0x01c)) # (R/W) System Handlers Priority Registers
r.append(reg32('SHPR3', 0x020)) # (R/W) System Handlers Priority Registers
r.append(reg32('SHCSR', 0x024)) # (R/W) System Handler Control and State Register
r.append(reg32('CFSR', 0x028)) # (R/W) Configurable Fault Status Register
r.append(reg8('MMSR', 0x028)) # (R/W) MemManage Fault Status Register
r.append(reg8('BFSR', 0x029)) # (R/W) BusFault Status Register
r.append(reg16('UFSR', 0x02a)) # (R/W) UsageFault Status Register
r.append(reg32('HFSR', 0x02C)) # (R/W) HardFault Status Register
r.append(reg32('DFSR', 0x030)) # (R/W) Debug Fault Status Register
r.append(reg32('MMFAR', 0x034)) # (R/W) MemManage Fault Address Register
r.append(reg32('BFAR', 0x038)) # (R/W) BusFault Address Register
r.append(reg32('AFSR', 0x03C)) # (R/W) Auxiliary Fault Status Register
r.append(reg32('PFR[0]', 0x040)) # (R/ ) Processor Feature Register
r.append(reg32('PFR[1]', 0x044)) # (R/ ) Processor Feature Register
r.append(reg32('DFR', 0x048)) # (R/ ) Debug Feature Register
r.append(reg32('ADR', 0x04C)) # (R/ ) Auxiliary Feature Register
r.append(reg32('MMFR[0]', 0x050)) # (R/ ) Memory Model Feature Register
r.append(reg32('MMFR[1]', 0x054)) # (R/ ) Memory Model Feature Register
r.append(reg32('MMFR[2]', 0x058)) # (R/ ) Memory Model Feature Register
r.append(reg32('MMFR[3]', 0x05c)) # (R/ ) Memory Model Feature Register
r.append(reg32('ISAR[0]', 0x060)) # (R/ ) Instruction Set Attributes Register
r.append(reg32('ISAR[1]', 0x064)) # (R/ ) Instruction Set Attributes Register
r.append(reg32('ISAR[2]', 0x068)) # (R/ ) Instruction Set Attributes Register
r.append(reg32('ISAR[3]', 0x06c)) # (R/ ) Instruction Set Attributes Register
r.append(reg32('ISAR[4]', 0x070)) # (R/ ) Instruction Set Attributes Register
r.append(reg32('CPACR', 0x088)) # (R/W) Coprocessor Access Control Register
scb_m4_regs = regset('SCB for Cortex-M4', r)

r = []
r.append(reg32('CPUID', 0x000, CPUID_fields)) # (R/ ) CPUID Base Register
r.append(reg32('ICSR', 0x004)) # (R/W) Interrupt Control and State Register
r.append(reg32('VTOR', 0x008)) # (R/W) Vector Table Offset Register
r.append(reg32('AIRCR', 0x00C)) # (R/W) Application Interrupt and Reset Control Register
r.append(reg32('SCR', 0x010)) # (R/W) System Control Register
r.append(reg32('CCR', 0x014)) # (R/W) Configuration Control Register
r.append(reg8('SHPR', 0x018, None)) # base register for access
r.append(reg32('SHPR2', 0x01c)) # (R/W) System Handlers Priority Registers
r.append(reg32('SHPR3', 0x020)) # (R/W) System Handlers Priority Registers
r.append(reg32('SHCSR', 0x024)) # (R/W) System Handler Control and State Register
scb_m0_plus_regs = regset('SCB for Cortex-M0+', r)

scb_regs = {
  'cortex-m4': (scb_m4_regs, SCB_BASE),
  'cortex-m0+': (scb_m0_plus_regs, SCB_BASE),
}

# -----------------------------------------------------------------------------
# Memory Protection Unit

r = []
r.append(reg32('TYPE', 0x000)) # (R/ ) MPU Type Register
r.append(reg32('CTRL', 0x004)) # (R/W) MPU Control Register
r.append(reg32('RNR', 0x008)) # (R/W) MPU Region RNRber Register
r.append(reg32('RBAR', 0x00C)) # (R/W) MPU Region Base Address Register
r.append(reg32('RASR', 0x010)) # (R/W) MPU Region Attribute and Size Register
r.append(reg32('RBAR_A1', 0x014)) # (R/W) MPU Alias 1 Region Base Address Register
r.append(reg32('RASR_A1', 0x018)) # (R/W) MPU Alias 1 Region Attribute and Size Register
r.append(reg32('RBAR_A2', 0x01C)) # (R/W) MPU Alias 2 Region Base Address Register
r.append(reg32('RASR_A2', 0x020)) # (R/W) MPU Alias 2 Region Attribute and Size Register
r.append(reg32('RBAR_A3', 0x024)) # (R/W) MPU Alias 3 Region Base Address Register
r.append(reg32('RASR_A3', 0x028)) # (R/W) MPU Alias 3 Region Attribute and Size Register
mpu_m4_regs = regset('MPU for Cortex-M4', r)

r = []
r.append(reg32('TYPE', 0x000)) # (R/ ) MPU Type Register
r.append(reg32('CTRL', 0x004)) # (R/W) MPU Control Register
r.append(reg32('RNR', 0x008)) # (R/W) MPU Region RNRber Register
r.append(reg32('RBAR', 0x00C)) # (R/W) MPU Region Base Address Register
r.append(reg32('RASR', 0x010)) # (R/W) MPU Region Attribute and Size Register
mpu_m0_plus_regs = regset('MPU for Cortex-M0+', r)

mpu_regs = {
  'cortex-m4': (mpu_m4_regs, MPU_BASE),
  'cortex-m0+': (mpu_m0_plus_regs, MPU_BASE),
}

# -----------------------------------------------------------------------------
# Floating Point Unit

r = []
r.append(reg32('FPCCR', 0x004)) # (R/W) Floating-Point Context Control Register
r.append(reg32('FPCAR', 0x008)) # (R/W) Floating-Point Context Address Register
r.append(reg32('FPDSCR', 0x00C)) # (R/W) Floating-Point Default Status Control Register
r.append(reg32('MVFR0', 0x010)) # (R/ ) Media and FP Feature Register 0
r.append(reg32('MVFR1', 0x014)) # (R/ ) Media and FP Feature Register 1
fpu_m4_regs = regset('Floating Point Unit', r)

fpu_regs = {
  'cortex-m4': (fpu_m4_regs, FPU_BASE),
}

# -----------------------------------------------------------------------------
# Nested Vectored Interrupt Controller

r = []
r.append(reg32('ISER0', 0x000)) # (R/W) Interrupt Set Enable Register
r.append(reg32('ISER1', 0x004)) # (R/W) Interrupt Set Enable Register
r.append(reg32('ISER2', 0x008)) # (R/W) Interrupt Set Enable Register
r.append(reg32('ISER3', 0x00c)) # (R/W) Interrupt Set Enable Register
r.append(reg32('ISER4', 0x010)) # (R/W) Interrupt Set Enable Register
r.append(reg32('ISER5', 0x014)) # (R/W) Interrupt Set Enable Register
r.append(reg32('ISER6', 0x018)) # (R/W) Interrupt Set Enable Register
r.append(reg32('ISER7', 0x01c)) # (R/W) Interrupt Set Enable Register
r.append(reg32('ICER0', 0x080)) # (R/W) Interrupt Clear Enable Register
r.append(reg32('ICER1', 0x084)) # (R/W) Interrupt Clear Enable Register
r.append(reg32('ICER2', 0x088)) # (R/W) Interrupt Clear Enable Register
r.append(reg32('ICER3', 0x08c)) # (R/W) Interrupt Clear Enable Register
r.append(reg32('ICER4', 0x090)) # (R/W) Interrupt Clear Enable Register
r.append(reg32('ICER5', 0x094)) # (R/W) Interrupt Clear Enable Register
r.append(reg32('ICER6', 0x098)) # (R/W) Interrupt Clear Enable Register
r.append(reg32('ICER7', 0x09c)) # (R/W) Interrupt Clear Enable Register
r.append(reg32('ISPR0', 0x100)) # (R/W) Interrupt Set Pending Register
r.append(reg32('ISPR1', 0x104)) # (R/W) Interrupt Set Pending Register
r.append(reg32('ISPR2', 0x108)) # (R/W) Interrupt Set Pending Register
r.append(reg32('ISPR3', 0x10c)) # (R/W) Interrupt Set Pending Register
r.append(reg32('ISPR4', 0x110)) # (R/W) Interrupt Set Pending Register
r.append(reg32('ISPR5', 0x114)) # (R/W) Interrupt Set Pending Register
r.append(reg32('ISPR6', 0x118)) # (R/W) Interrupt Set Pending Register
r.append(reg32('ISPR7', 0x11c)) # (R/W) Interrupt Set Pending Register
r.append(reg32('ICPR0', 0x180)) # (R/W) Interrupt Clear Pending Register
r.append(reg32('ICPR1', 0x184)) # (R/W) Interrupt Clear Pending Register
r.append(reg32('ICPR2', 0x188)) # (R/W) Interrupt Clear Pending Register
r.append(reg32('ICPR3', 0x18c)) # (R/W) Interrupt Clear Pending Register
r.append(reg32('ICPR4', 0x190)) # (R/W) Interrupt Clear Pending Register
r.append(reg32('ICPR5', 0x194)) # (R/W) Interrupt Clear Pending Register
r.append(reg32('ICPR6', 0x198)) # (R/W) Interrupt Clear Pending Register
r.append(reg32('ICPR7', 0x19c)) # (R/W) Interrupt Clear Pending Register
r.append(reg32('IABR0', 0x200)) # (R/W) Interrupt Active bit Register
r.append(reg32('IABR1', 0x204)) # (R/W) Interrupt Active bit Register
r.append(reg32('IABR2', 0x208)) # (R/W) Interrupt Active bit Register
r.append(reg32('IABR3', 0x20c)) # (R/W) Interrupt Active bit Register
r.append(reg32('IABR4', 0x210)) # (R/W) Interrupt Active bit Register
r.append(reg32('IABR5', 0x214)) # (R/W) Interrupt Active bit Register
r.append(reg32('IABR6', 0x218)) # (R/W) Interrupt Active bit Register
r.append(reg32('IABR7', 0x21c)) # (R/W) Interrupt Active bit Register
r.append(reg8('IPR', 0x300, None)) # byte access
r.append(reg32('IPR0', 0x300)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR1', 0x304)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR2', 0x308)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR3', 0x30c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR4', 0x310)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR5', 0x314)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR6', 0x318)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR7', 0x31c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR8', 0x320)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR9', 0x324)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR10', 0x328)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR11', 0x32c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR12', 0x330)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR13', 0x334)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR14', 0x338)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR15', 0x33c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR16', 0x340)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR17', 0x344)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR18', 0x348)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR19', 0x34c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR20', 0x350)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR21', 0x354)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR22', 0x358)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR23', 0x35c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR24', 0x360)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR25', 0x364)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR26', 0x368)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR27', 0x36c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR28', 0x370)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR29', 0x374)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR30', 0x378)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR31', 0x37c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR32', 0x380)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR33', 0x384)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR34', 0x388)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR35', 0x38c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR36', 0x390)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR37', 0x394)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR38', 0x398)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR39', 0x39c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR40', 0x3a0)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR41', 0x3a4)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR42', 0x3a8)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR43', 0x3ac)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR44', 0x3b0)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR45', 0x3b4)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR46', 0x3b8)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR47', 0x3bc)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR48', 0x3c0)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR49', 0x3c4)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR50', 0x3c8)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR51', 0x3cc)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR52', 0x3d0)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR53', 0x3d4)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR54', 0x3d8)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR55', 0x3dc)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR56', 0x3e0)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR57', 0x3e4)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR58', 0x3e8)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR59', 0x3ec)) # (R/W) Interrupt Priority Register
r.append(reg32('STIR', 0xe00)) #( /W) Software Trigger Interrupt Register
nvic_m4_regs = regset('NVIC for Cortex-M4', r)

r = []
r.append(reg32('ISER0', 0x000)) # (R/W) Interrupt Set Enable Register
r.append(reg32('ICER0', 0x080)) # (R/W) Interrupt Clear Enable Register
r.append(reg32('ISPR0', 0x100)) # (R/W) Interrupt Set Pending Register
r.append(reg32('ICPR0', 0x180)) # (R/W) Interrupt Clear Pending Register
r.append(reg32('IABR0', 0x200, None)) # not implemented on cortex-m0+
r.append(reg8('IPR', 0x300, None)) # byte access
r.append(reg32('IPR0', 0x300)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR1', 0x304)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR2', 0x308)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR3', 0x30c)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR4', 0x310)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR5', 0x314)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR6', 0x318)) # (R/W) Interrupt Priority Register
r.append(reg32('IPR7', 0x31c)) # (R/W) Interrupt Priority Register
nvic_m0_plus_regs = regset('NVIC for Cortex-M0+', r)

nvic_regs = {
  'cortex-m4': (nvic_m4_regs, NVIC_BASE),
  'cortex-m0+': (nvic_m0_plus_regs, NVIC_BASE),
}

# -----------------------------------------------------------------------------

def memory_test(ui, cpu, adr, block_size, num_blocks, iters):
  """test ram memory over a given region"""
  # test a 32 bit write at the start and end of the block
  locns = [adr + (block_size * i) for i in range(num_blocks)]
  locns.extend([adr - 4 + (block_size * (i + 1)) for i in range(num_blocks)])
  max_adr = adr + (block_size * num_blocks) - 4
  ui.put('testing %d locations %08x-%08x (32 bit write/read, %d iterations)\n' % (len(locns), adr, max_adr, iters))

  for i in range(iters):
    # writing random values
    ui.put('%d: writing...\n' % i)
    saved = []
    for adr in locns:
      val = random.getrandbits(32)
      cpu.wr(adr, val, 32)
      saved.append(val)
    # reading back values
    ui.put('%d: reading...\n' % i)
    bad = 0
    for (adr, wr_val) in zip(locns, saved):
      val = cpu.rd(adr, 32)
      if val != wr_val:
        ui.put('[%08x] = %08x : should be %08x, xor %08x\n' % (adr, val, wr_val, val ^ wr_val))
        bad += 1
    # report for this iteration
    if not bad:
      ui.put('%d: passed\n' % i)
    else:
      ui.put('%d: %d of %d locations failed\n' % (i, bad, len(locns)))

# -----------------------------------------------------------------------------

class cortexm(object):

  def __init__(self, target, ui, jlink, cpu_type, priority_bits):
    self.target = target
    self.ui = ui
    self.jlink = jlink
    self.cpu_type = cpu_type
    self.priority_bits = priority_bits
    self.saved_regs = []
    self.width = 32

    # setup the memory mapped registers for this cpu
    self.scb = self.get_memio(scb_regs)
    self.systick = self.get_memio(systick_regs)
    self.nvic = self.get_memio(nvic_regs)

    self.menu_memory = (
      ('display', 'dump memory to display', self.cmd_mem2display, _help_memdisplay),
      ('>file', 'read from memory, write to file', self.cmd_mem2file, _help_mem2file),
      #('<file', 'read from file, write to memory', self.cmd_file2mem, _help_file2mem),
      ('rd8', 'read 8 bits', self.cmd_rd8, _help_memrd),
      ('rd16', 'read 16 bits', self.cmd_rd16, _help_memrd),
      ('rd32', 'read 32 bits', self.cmd_rd32, _help_memrd),
      ('test', 'read/write test of memory', self.cmd_memtest),
      #('verify', 'verify memory against a file', self.cmd_verify, _help_file2mem),
      ('wr8', 'write 8 bits', self.cmd_wr8, _help_memwr),
      ('wr16', 'write 16 bits', self.cmd_wr16, _help_memwr),
      ('wr32', 'write 32 bits', self.cmd_wr32, _help_memwr),
    )
    self.menu_cpu = (
      ('fpu', 'floating point unit registers', self.cmd_fpu),
      ('mpu', 'memory protection unit registers', self.cmd_mpu),
      ('nvic', 'nested vectored interrupt controller registers', self.cmd_nvic),
      ('scb', 'system control block registers', self.cmd_scb),
      ('systick', 'systick registers', self.cmd_systick),
      ('rate', 'measure systick counter rate', self.cmd_systick_rate),
    )

  def get_memio(self, x_regs):
    """return a memory accessor for a given register set"""
    (regs, base) = x_regs[self.cpu_type]
    return memio(regs, self, base)

  def rd(self, adr, n):
    """read from memory - n bits aligned"""
    adr = util.align_adr(adr, n)
    if n == 32:
      return self.jlink.rd32(adr)
    elif n == 16:
      return self.jlink.rd16(adr)
    elif n == 8:
      return self.jlink.rd8(adr)
    else:
      return 0

  def wr(self, adr, val, n):
    """write to memory - n bits aligned"""
    adr = util.align_adr(adr, n)
    if n == 32:
      return self.jlink.wr32(adr, val)
    elif n == 16:
      return self.jlink.wr16(adr, val)
    elif n == 8:
      return self.jlink.wr8(adr, val)
    else:
      return 0

  def rd_mem(self, adr, n, io):
    """read n 32 bit words from memory starting at adr"""
    max_words = 16
    while n > 0:
      nwords = (n, max_words)[n >= max_words]
      [io.write(x) for x in self.jlink.rdmem32(adr, nwords)]
      n -= nwords
      adr += nwords * 4

  def wr_mem(self, adr, n, io):
    """write n 32 bit words to memory starting at adr"""
    self.jlink.wrmem32(adr, [io.read() for i in range(n)])

  def halt(self, msg=False):
    """halt the cpu"""
    if self.jlink.is_halted():
      if msg:
        self.ui.put('cpu is already halted\n')
      return
    self.jlink.halt()
    self.target.set_prompt()

  def go(self, msg=False):
    """un-halt the cpu"""
    if not self.jlink.is_halted():
      if msg:
        self.ui.put('cpu is already running\n')
      return
    self.jlink.go()
    self.target.set_prompt()

  def reset(self):
    """reset the cpu"""
    self.jlink.reset()

  def step(self):
    """single step the cpu"""
    self.jlink.step()

  def NVIC_GetPriority(self, irq):
    """return the priority encoding for an exception"""
    if irq == Reset_IRQn:
      return -3
    elif irq == NMI_IRQn:
      return -2
    elif irq == HardFault_IRQn:
      return -1
    elif irq < 0:
      # system exceptions
      return self.scb.rd('SHPR', irq + NUM_SYS_EXC - 4) >> (8 - self.priority_bits)
    else:
      # interrupt handlers
      return self.nvic.rd('IPR', irq) >> (8 - self.priority_bits)

  def NVIC_GetPriorityGrouping(self):
    """return the priority grouping number"""
    (regs, base) = scb_regs[self.cpu_type]
    scb = memio(regs, self, base)
    return (scb.rd('AIRCR') >> 8) & 7

  def NVIC_DecodePriority(self, priority, group):
    """decode a priority level"""
    group &= 7
    pre_bits = (7 - group, self.priority_bits)[(7 - group) > self.priority_bits]
    sub_bits = self.priority_bits - pre_bits
    pre = (priority >> sub_bits) & ((1 << (pre_bits)) - 1)
    sub = priority & ((1 << sub_bits) - 1)
    return (pre, sub)

  def NVIC_DecodeString(self, group):
    """return a priority decode string"""
    group &= 7
    pre_bits = (7 - group, self.priority_bits)[(7 - group) > self.priority_bits]
    sub_bits = self.priority_bits - pre_bits
    s = []
    s.append('p' * pre_bits)
    s.append('s' * sub_bits)
    s.append('.' * (8 - pre_bits - sub_bits))
    s.append(' %d bits group %d' % (self.priority_bits, group))
    return ''.join(s)

  def cmd_rd(self, ui, args, n):
    """memory read command for n bits"""
    if util.wrong_argc(ui, args, (1,)):
      return
    adr = util.sex_arg(ui, args[0], self.width)
    if adr == None:
      return
    adr = util.align_adr(adr, n)
    ui.put('[0x%08x] = ' % adr)
    ui.put('0x%%0%dx\n' % (n/4) % self.rd(adr, n))

  def cmd_rd8(self, ui, args):
    """read 8 bits"""
    self.cmd_rd(ui, args, 8)

  def cmd_rd16(self, ui, args):
    """read 16 bits"""
    self.cmd_rd(ui, args, 16)

  def cmd_rd32(self, ui, args):
    """read 32 bits"""
    self.cmd_rd(ui, args, 32)

  def cmd_wr(self, ui, args, n):
    """memory write command for n bits"""
    if util.wrong_argc(ui, args, (1,2)):
      return
    adr = util.sex_arg(ui, args[0], self.width)
    if adr == None:
      return
    adr = util.align_adr(adr, n)
    val = 0
    if len(args) == 2:
      val = util.int_arg(ui, args[1], util.limit_32, 16)
      if val == None:
        return
    val = util.mask_val(val, n)
    self.wr(adr, val, n)
    ui.put('[0x%08x] = ' % adr)
    ui.put('0x%%0%dx\n' % (n/4) % val)

  def cmd_wr8(self, ui, args):
    """write 8 bits"""
    self.cmd_wr(ui, args, 8)

  def cmd_wr16(self, ui, args):
    """write 16 bits"""
    self.cmd_wr(ui, args, 16)

  def cmd_wr32(self, ui, args):
    """write 32 bits"""
    self.cmd_wr(ui, args, 32)

  def cmd_mem2file(self, ui, args):
    """dump memory contents to a file"""
    x = util.m2f_args(ui, 32, args)
    if x is None:
      return
    (adr, n, name) = x
    # adjust the address and length
    adr = util.align_adr(adr, 32)
    n = util.nbytes_to_nwords(n, 32)
    # read memory, write to file object
    mf = io.to_file(32, ui, name, n, le=True)
    self.rd_mem(adr, n, mf)
    mf.close()

  def cmd_user_registers(self, ui, args):
    """display the arm user registers"""
    self.halt()
    regs = [self.jlink.rdreg(n) for (name, n) in _reg_names]
    if len(self.saved_regs) == 0:
      self.saved_regs = regs
    delta = [('*', '')[x == y] for (x, y) in zip(self.saved_regs, regs)]
    self.saved_regs = regs
    for i in range(len(_reg_names)):
      ui.put('%-8s: %08x %s\n' % (_reg_names[i][0], regs[i], delta[i]))

  def cmd_mem2display(self, ui, args):
    """display memory"""
    x = util.m2d_args(ui, 32, args)
    if x is None:
      return
    (adr, n) = x
    # address is on a 16 byte boundary
    # n is an integral multiple of 16 bytes
    adr &= ~15
    n = (n + 15) & ~15
    n = util.nbytes_to_nwords(n, 32)
    # read memory, dump to display
    md = io.to_display(32, ui, adr, le=True)
    self.rd_mem(adr, n, md)

  def cmd_memtest(self, ui, args):
    """test memory"""
    block_size = util.MiB / 4
    memory_test(ui, self, self.target.ram_start, block_size, self.target.ram_size / block_size, 8)

  def cmd_disassemble(self, ui, args):
    """disassemble memory"""
    if util.wrong_argc(ui, args, (0, 1, 2)):
      return
    n = 16
    if len(args) == 0:
      # read the pc
      self.halt()
      adr = self.jlink.rd_pc()
    if len(args) >= 1:
      adr = util.sex_arg(ui, args[0], 32)
      if adr is None:
        return
    if len(args) == 2:
      n = util.int_arg(ui, args[1], (1, 2048), 16)
      if n is None:
        return
    # align the address to 32 bits
    adr = util.align_adr(adr, 32)
    # disassemble
    md = io.arm_disassemble(ui, adr)
    self.rd_mem(adr, n, md)

  def cmd_go(self, ui, args):
    self.go(msg=True)

  def cmd_halt(self, ui, args):
    self.halt(msg=True)

  def cmd_step(self, ui, args):
    self.step()

  def display_regs(self, ui, regs_by_type):
    """display a register set by cpu type"""
    if regs_by_type.has_key(self.cpu_type):
      (regs, base) = regs_by_type[self.cpu_type]
      ui.put('%s\n' % regs.emit(self, base))
    else:
      ui.put('not defined for %s\n' % self.cpu_type)

  def cmd_systick(self, ui, args):
    """display systick registers"""
    self.display_regs(ui, systick_regs)

  def cmd_scb(self, ui, args):
    """display system control block registers"""
    self.display_regs(ui, scb_regs)

  def cmd_fpu(self, ui, args):
    """display floating point unit registers"""
    if self.cpu_type in ('cortex-m0+',):
      ui.put('%s devices do not have an fpu\n' % self.cpu_type)
    else:
      self.display_regs(ui, fpu_regs)

  def cmd_mpu(self, ui, args):
    """display memory protection unit registers"""
    self.display_regs(ui, mpu_regs)

  def cmd_nvic(self, ui, args):
    """display nested vectored interrupt controller registers"""
    self.display_regs(ui, nvic_regs)

  def systick_rate(self, t, cpuclk):
    """return the systick count after t seconds"""
    self.halt()
    # save the current settings
    saved_ctrl = self.systick.rd('CTRL')
    saved_load = self.systick.rd('LOAD')
    saved_val = self.systick.rd('VAL')
    # setup systick
    self.systick.wr('CTRL', (cpuclk << 2) | (1 << 0))
    self.systick.wr('VAL', SysTick_MAXCOUNT)
    self.systick.wr('LOAD', SysTick_MAXCOUNT)
    # run for a while
    self.go()
    t_start = time.time()
    time.sleep(t)
    t = time.time() - t_start
    self.halt()
    # read the counter
    stop = self.systick.rd('VAL')
    # restore the saved settings
    self.systick.wr('VAL', saved_val)
    self.systick.wr('LOAD', saved_load)
    self.systick.wr('CTRL', saved_ctrl)
    # return the tick count and time
    return (SysTick_MAXCOUNT - stop, t)

  def measure_systick(self, ui, msg, cpuclk):
    """measure systick rate"""
    ui.put('%s clock rate: ' % msg)
    # short trial measurement that hopefully will not underflow
    (c, t) = self.systick_rate(0.05, cpuclk)
    if c:
      # longer measurement for better accuracy
      t = 0.8 * t * float(SysTick_MAXCOUNT) / float(c)
      # clamp the time to a maximum limit
      if t > 4:
        t = 4
      (c, t) = self.systick_rate(t, cpuclk)
      mhz = c / (1000000 * t)
      ui.put('%.2f Mhz\n' % mhz)
    else:
      ui.put('fail: systick did not decrement\n')

  def cmd_systick_rate(self, ui, args):
    self.measure_systick(ui, 'external', 0)
    self.measure_systick(ui, 'cpu', 1)

# -----------------------------------------------------------------------------
# return a string for the current state of the exceptions
# This is a generic CPU function but to do this properly we need some information
# from the SoC. So- this function is not a part of the cpu object.

system_exceptions = {
  1: 'Reset',
  2: 'NMI',
  3: 'HardFault',
  4: 'MemManage',
  5: 'BusFault',
  6: 'UsageFault',
  11: 'SVCall',
  12: 'DebugMonitor',
  14: 'PendSV',
  15: 'SysTick',
}

NUM_SYS_EXC = 16

Reset_IRQn = -15
NMI_IRQn = -14
HardFault_IRQn = -13
MemManage_IRQn = -12
BusFault_IRQn = -11
UsageFault_IRQn = -10
SVCall_IRQn = -5
DebugMonitor_IRQn = -4
PendSV_IRQn = -2
SysTick_IRQn = -1

def build_exceptions(vector_table):
  """combine the system exceptions with an SoC irq vector table"""
  d = dict(system_exceptions)
  for (k, v) in vector_table.iteritems():
    d[k + NUM_SYS_EXC] = v
  return d

def exceptions_str(cpu, soc):
  s = []
  group = cpu.NVIC_GetPriorityGrouping()
  vtable = cpu.scb.rd('VTOR')
  icsr = cpu.scb.rd('ICSR')
  shcsr = cpu.scb.rd('SHCSR')

  s.append('%-19s: %s' % ('priority grouping', cpu.NVIC_DecodeString(group)))
  s.append('%-19s: %08x' % ('vector table', vtable))
  s.append('Name                 Exc Irq EPA Prio Vector')
  for i in sorted(soc.exceptions.keys()):
    l = []
    irq = i - NUM_SYS_EXC

    # name
    l.append('%-19s: ' % soc.exceptions[i])
    # exception number
    l.append('%-3d ' % i)
    # irq number
    l.append(('-   ', '%-3d ' % irq)[irq >= 0])

    # enabled/pending/active
    enabled = pending = active = -1
    if irq >= 0:
      idx = (irq >> 5) & 7
      shift = irq & 31
      enabled = (cpu.nvic.rd('ISER0', idx) >> shift) & 1
      pending = (cpu.nvic.rd('ISPR0', idx) >> shift) & 1
      active = (cpu.nvic.rd('IABR0', idx) >> shift) & 1
    else:
      if irq == NMI_IRQn:
        enabled = 1
        pending = (icsr >> 31) & 1
      elif irq == MemManage_IRQn:
        enabled = (shcsr >> 16) & 1
        pending = (shcsr >> 13) & 1
        active = (shcsr >> 0) & 1
      elif irq == BusFault_IRQn:
        enabled = (shcsr >> 17) & 1
        pending = (shcsr >> 14) & 1
        active = (shcsr >> 1) & 1
      elif irq == UsageFault_IRQn:
        enabled = (shcsr >> 18) & 1
        pending = (shcsr >> 12) & 1
        active = (shcsr >> 3) & 1
      elif irq == SVCall_IRQn:
        pending = (shcsr >> 15) & 1
        active = (shcsr >> 7) & 1
      elif irq == DebugMonitor_IRQn:
        active = (shcsr >> 8) & 1
      elif irq == PendSV_IRQn:
        pending = (icsr >> 28) & 1
      elif irq == SysTick_IRQn:
        enabled = (cpu.systick.rd('CTRL') >> 1) & 1
        pending = (icsr >> 26) & 1
    l.append(util.format_bit(enabled, 'e'))
    l.append(util.format_bit(pending, 'p'))
    l.append(util.format_bit(active, 'a'))
    l.append(' ')

    # priority
    priority = cpu.NVIC_GetPriority(irq)
    if priority < 0:
      tmp = '%-4d' % priority
    else:
      tmp = '%d.%d' % cpu.NVIC_DecodePriority(priority, group)
    l.append('%-4s ' % tmp)

    # vector
    l.append('%08x ' % (cpu.rd(vtable + (i * 4), 32) & ~1))
    s.append(''.join(l))
  return '\n'.join(s)

# -----------------------------------------------------------------------------
