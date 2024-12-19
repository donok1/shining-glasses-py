from ble import adapter
from driver import ShiningGlassesDriver
from shining_glasses import ShiningGlasses

if __name__ == "__main__":
    driver = ShiningGlassesDriver(adapter)
    driver.connect()

    glasses = ShiningGlasses(driver)
    glasses.set_light(brightness=100)
    glasses.set_image(img_idx=0)
    glasses.play(n_imgs=1, img_idcs=[0])