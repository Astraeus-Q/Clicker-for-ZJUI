#include "keybrd.h"
#include "oled.h"
#include "stm32f1xx_hal.h"

void UI_welcome()
{
    OLED_CLS();
    OLED_ShowStr(0,2," IClicker ZJU ",2);
    OLED_ShowStr(30,6," Ver 1.2  ",2);

}

void UI_default(struct KEYBRD_INFO *keybrd_info, int8_t if_sending){
    if (keybrd_info->display_answer == 0)
    {
        OLED_ShowStr(10,0,"Please input ",2);
        OLED_ShowStr(10,4,"your answer",2);
    }

    if (keybrd_info->display_answer == 1)
    {
        if (keybrd_info->current_answer == 0)
        {
            OLED_ShowStr(20,6,"SEND SUCCESSFUL",1);
        }
        else
        {
            OLED_ShowStr(10,0,"Answer: A",2);
        }
    }

    if (keybrd_info->display_answer == 2)
    {
        if (keybrd_info->current_answer == 0)
        {
            OLED_ShowStr(20,6,"SEND SUCCESSFUL",1);
        }
        else
        {
            OLED_ShowStr(10,0,"Answer: B",2);
        }
    }

    if (keybrd_info->display_answer == 3)
    {
        if (keybrd_info->current_answer == 0)
        {
            OLED_ShowStr(20,6,"SEND SUCCESSFUL",1);
        }
        else
        {
            OLED_ShowStr(10,0,"Answer: C",2);
        }
    }

    if (keybrd_info->display_answer == 4)
    {
        if (keybrd_info->current_answer == 0)
        {
            OLED_ShowStr(20,6,"SEND SUCCESSFUL",1);
        }
        else
        {
            OLED_ShowStr(10,0,"Answer: D",2);
        }
    }
    
    if (if_sending == 1)
    {
        OLED_ShowStr(20,4,"SENDING...",2);
    }
    

}