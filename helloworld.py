import thorpy, pygame

def run():

    # Creating the application - 1st step
    application = thorpy.Application((1366, 768), "ThorPy Overview")

    # Universal appearance for all the buttons in the unclicked state
    default_painter = thorpy.painters.roundrect.RoundRect(size=(300,70),
                                                 color=(55,255,55),
                                                 radius=0.3)

    # Universal appearance for all the buttons in the clicked state
    onclick_painter = thorpy.painters.roundrect.RoundRect(size=(300,70),
                                                 color=(55,255,55),
                                                 radius=0.3)

    # Button to read value from load cell and display it on the screen
    def loadcell_read(event):
        print("Load Cell Reading:", event.pos)
    loadcell_reaction = thorpy.Reaction(reacts_to=pygame.MOUSEBUTTONDOWN, reac_func=loadcell_read)
    loadcell = thorpy.Clickable("Load Cell", press_params={"painter":onclick_painter})
    thorpy.makeup.add_basic_help(loadcell,"Power on load cell, retrieve reading from load \n cell, and display the reading on the screen.")
    loadcell.finish()
    loadcell.add_reaction(loadcell_reaction)

    # Button to read value from IMU and display it on the screen
    def imu_read(event):
        print("Accelerometer Reading:", event.pos)
        print("Gyroscope Reading:", event.pos)
    imu_reaction = thorpy.Reaction(reacts_to=pygame.MOUSEBUTTONDOWN, reac_func=imu_read)
    imu = thorpy.Clickable("IMU")
    thorpy.makeup.add_basic_help(imu,"Power on the IMU, retrieve readings from its accelerometer \n and gyroscope components, and display the readings on the screen.")
    imu.finish()
    imu.add_reaction(imu_reaction)

    # Button to capture images using camera and servo, process the images, compute for the intensity of foaming, and 
    # display it on the screen
    
    # Button to exit the application
    quit = thorpy.make_button("Quit", func=thorpy.functions.quit_menu_func)
    thorpy.makeup.add_basic_help(quit,"Exits the application.")

    # Arranging the elements on screen
    title_element = thorpy.make_text("Anaerobic Digester Sample Tester Prototype", 22, (0,0,0))
    elements = [loadcell, imu, quit]
    central_box = thorpy.Box(elements=elements)
    central_box.fit_children(margins=(100,100)) #we want big margins
    central_box.center() #center on screen
    central_box.set_main_color((220,220,220,180)) #set box color and opacity

    # Background for the application
    background = thorpy.Background.make(color=(200, 200, 255),
                                    elements=[title_element, central_box])
    thorpy.store(background)

    menu = thorpy.Menu(background)
    menu.play()

    application.quit()



if __name__ == "__main__":
    run()
