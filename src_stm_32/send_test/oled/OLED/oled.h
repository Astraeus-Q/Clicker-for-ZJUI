#ifndef __OLED_H
#define __OLED_H	 

#include "type.h" 
 #define u8 uint8_t
 #define u32 uint32_t
 
 
 void DATAOUT(unsigned int data);
 
 #define OLED_RD_H HAL_GPIO_WritePin(GPIOD, GPIO_PIN_10, GPIO_PIN_SET) 
#define OLED_RD_L HAL_GPIO_WritePin(GPIOD, GPIO_PIN_10, GPIO_PIN_RESET) 
//#define OLED_WR  PDout(11)	

#define OLED_WR_H HAL_GPIO_WritePin(GPIOD, GPIO_PIN_11, GPIO_PIN_SET) 
#define OLED_WR_L HAL_GPIO_WritePin(GPIOD, GPIO_PIN_11, GPIO_PIN_RESET) 

//#define OLED_RS  PDout(12)

#define OLED_DC_H HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12, GPIO_PIN_SET) 
#define OLED_DC_L HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12, GPIO_PIN_RESET) 

//#define OLED_RST PDout(13) 	
#define OLED_RST_H HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13, GPIO_PIN_SET) 
#define OLED_RST_L HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13, GPIO_PIN_RESET) 

//#define OLED_CS  PDout(14)

#define OLED_CS_H HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, GPIO_PIN_SET) 
#define OLED_CS_L HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, GPIO_PIN_RESET) 
//    ??????
//		OLED_ShowStr(0, 0, "hello world", 2);//?????
//	  OLED_ShowStr(0, 2, "hello world", 1);//?????
//	  OLED_ShowCN_STR(0, 4 , 0 , 8);
//		sprintf(num_temp_buffer,"show num:%0.2f",num);
//		OLED_ShowStr(0, 6, num_temp_buffer, 2);//?????
//		OLED_CLS();
//		OLED_DrawBMP(0,0,128,7,BMP2);

#define OLED0561_ADD	0x78  // OLED?I2C??(????)
#define COM				0x00  // OLED ??(????)
#define DAT 			0x40  // OLED ??(????)

void WriteCmd(unsigned char I2C_Command);//???
void WriteDat(unsigned char I2C_Data);//???
void OLED_Init(void);//???
void OLED_SetPos(unsigned char x, unsigned char y);
void OLED_Fill(unsigned char fill_Data);//????
void OLED_CLS(void);
void OLED_ON(void);
void OLED_OFF(void);
void OLED_ShowStr(unsigned char x, unsigned char y, unsigned char ch[], unsigned char TextSize);//?????
void OLED_ShowCN(unsigned char x, unsigned char y, unsigned char N);//????
void OLED_DrawBMP(unsigned char x0,unsigned char y0,unsigned char x1,unsigned char y1,unsigned char BMP[]);//??????(??????)

void OLED_ShowCN_STR(u8 x , u8 y , u8 begin , u8 num);  //???????????

void OLED_ShowChar(u8 x,u8 y,u8 chr,u8 Char_Size);
u32 oled_pow(u8 m,u8 n);
void OLED_ShowNum(u8 x,u8 y,u32 num,u8 len,u8 size2);//size2(16|12)
void OLED_DrawGIF(unsigned char x0, unsigned char y0,unsigned char x1, unsigned char y1, unsigned char k, int m, unsigned char GIF[][m]);

#endif
