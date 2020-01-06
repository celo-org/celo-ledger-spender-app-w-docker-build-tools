#![no_std]

use core::panic::PanicInfo;

#[no_mangle]
pub extern fn test_sign() -> char {
  'x'
}

/// This function is called on panic.
#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
  loop {}
}
