#ifndef __KEYBRD_H
#define __KEYBRD_H

#include "type.h"



// define gpio pa9-pa12 as keyborad row output
#define KEYBRD_ROW_0_H HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9, GPIO_PIN_SET);
#define KEYBRD_ROW_0_L HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9, GPIO_PIN_RESET);

#define KEYBRD_ROW_1_H HAL_GPIO_WritePin(GPIOA, GPIO_PIN_10, GPIO_PIN_SET);
#define KEYBRD_ROW_1_L HAL_GPIO_WritePin(GPIOA, GPIO_PIN_10, GPIO_PIN_RESET);

#define KEYBRD_ROW_2_H HAL_GPIO_WritePin(GPIOA, GPIO_PIN_11, GPIO_PIN_SET);
#define KEYBRD_ROW_2_L HAL_GPIO_WritePin(GPIOA, GPIO_PIN_11, GPIO_PIN_RESET);

#define KEYBRD_ROW_3_H HAL_GPIO_WritePin(GPIOA, GPIO_PIN_12, GPIO_PIN_SET);
#define KEYBRD_ROW_3_L HAL_GPIO_WritePin(GPIOA, GPIO_PIN_12, GPIO_PIN_RESET);

// define gpio pe2-pe5 pin number
// #define KEY_0 GPIO_PIN_2;
// #define KEY_1 GPIO_PIN_3;
// #define KEY_2 GPIO_PIN_4;
// #define KEY_3 GPIO_PIN_5;

struct KEYBRD_INFO
{
    int8_t keypad_state[16];
    int8_t display_answer;
    int8_t current_answer;
};

void KEYBRD_Init();

void __KEYBRD_select(int8_t key);
void __KEYBRD_unselect();

int8_t __KEYBRD_read_instuction(int8_t flag, int8_t input);

void KEYBRD_Read(int8_t row, int8_t *current_state);

// u8 KEYBRD_Pin_Read(u16 PIN_NUM);

uint8_t KEYBRD_get_func(struct KEYBRD_INFO *k, uint8_t current_state);




// struct for 






#endif
