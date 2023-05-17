#include "keybrd.h"
#include "type.h"
#include "oled.h"

void KEYBRD_Init(){
    KEYBRD_ROW_0_H;
    KEYBRD_ROW_1_H;
    KEYBRD_ROW_2_H;
    KEYBRD_ROW_3_H;
}


void __KEYBRD_select(int8_t key){
    switch (key)
    {
    case 0:
        KEYBRD_ROW_0_L;
        break;
    case 1:
        KEYBRD_ROW_1_L;
        break;
    case 2:
        KEYBRD_ROW_2_L;
        break;
    case 3:
        KEYBRD_ROW_3_L;
        break;

    default:
        break;
    }
    
}

void __KEYBRD_unselect(){
    KEYBRD_Init();
}


int8_t __KEYBRD_read_instuction(int8_t flag, int8_t input)
{
    // state machine for the keypad instruction
    // state machine description:
    //      State 0: Button Free
    //      State -1: Button Release (Normally respond as CLICK)
    //      State 1-79: Button Pushed (normally the program won't respond to push operation)
    //      State 80: Button Hold (The button has been pushed continuously for 3 sec, reserved for speacial functions)
    if (flag == 0)
    {
        // if state 0
        if (input == 1)
        {
            // return state 1, pushed state
            return 1;
        }
        else
        {
            // return state 0, blank state
            return 0;
        }
    }
    else
    {
        // if state -1, 1-15
        if (flag >= 80 && input == 1)
        {
            // keeyp state 15 if input 1
            return 80;
        }
        if (flag >= 80 && input == 0)
        {
            return 0;
        }
        
        if (flag == -1 && input == 1)
        {
            // push the button after release, state 1
            return 1;
        }
        if (flag >= 2 && input == 0)
        {
            // button release, state -1
            return -1;
        }
        if (flag >= 0 && input == 0)
        {
            return 0;
        }
        
        
            // button been pushed or keep free, state++
            return flag + 1;
        
    }
}

void KEYBRD_Read(int8_t row, int8_t *current_state){
    __KEYBRD_select(row);

    u8 key_0 = HAL_GPIO_ReadPin(GPIOE, GPIO_PIN_5);
    u8 key_1 = HAL_GPIO_ReadPin(GPIOE, GPIO_PIN_4);
    u8 key_2 = HAL_GPIO_ReadPin(GPIOE, GPIO_PIN_3);
    u8 key_3 = HAL_GPIO_ReadPin(GPIOE, GPIO_PIN_2);

    __KEYBRD_unselect();

    u8 arr_key[4] = {key_0,key_1,key_2,key_3};

    for (int8_t i = 0; i < 4; i++)
    {
        int8_t input = 0;
        if (arr_key[i] == 1)
        {
            input = 0;
        }
        else
        {
            input = 1;
        }
        current_state[row * 4 + i] = __KEYBRD_read_instuction(current_state[row * 4 + i], input);
    } 
}

uint8_t KEYBRD_get_func(struct KEYBRD_INFO *keybrd_info, uint8_t current_state)
{

    uint8_t flag_clear = 1;
    if (keybrd_info->keypad_state[5] == -1)
    {
        keybrd_info->current_answer = 4;
        keybrd_info->display_answer = 4;
    }
    else if (keybrd_info->keypad_state[4] == -1)
    {
        keybrd_info->current_answer = 3;
        keybrd_info->display_answer = 3;
    }
    else if (keybrd_info->keypad_state[1] == -1)
    {
        keybrd_info->current_answer = 2;
        keybrd_info->display_answer = 2;
    }
    else if (keybrd_info->keypad_state[0] == -1)
    {
        keybrd_info->current_answer = 1;
        keybrd_info->display_answer = 1;
    }
    else
    {
    }  

    if (keybrd_info->keypad_state[6] == -1)
    {
        keybrd_info->current_answer = 0;
        keybrd_info->display_answer = 0;
        flag_clear = 0;
    }
    
    uint8_t ret = current_state & flag_clear;

    if (keybrd_info->keypad_state[2] == -1)
    {
        ret = 2;
    }
    
    return ret;
}
