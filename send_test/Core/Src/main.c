/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "spi.h"
#include "tim.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "oled.h"
#include "keybrd.h"
#include "user_interface.h"
#include "nrf24l01p.h"
#include <stdio.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
uint8_t rx_data[NRF24L01P_PAYLOAD_LENGTH] = {0};
uint8_t tx_data[NRF24L01P_PAYLOAD_LENGTH] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
//static void MX_GPIO_Init(void);
int8_t KEYBRD_Read_Row = 0;
int8_t KEYBRD_Read_En = 0;
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */
  HAL_Delay(1000);
  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_TIM6_Init();
  MX_SPI1_Init();
  /* USER CODE BEGIN 2 */
  
  UI_welcome();
  nrf24l01p_tx_init(2500, _250kbps);


  // TEST USE
	// char check[4];
  // if(nrf24l01p_check)
	// {
	// 	sprintf(check, "%d", 1);
	// }
	// else
	// {
	// 	sprintf(check, "%d", 0);
	// }
  // OLED_ShowStr(20,2,check,2);
	// HAL_Delay(2000);
  

  // uint8_t *bufl;
  // bufl = read_03();
  // for (int8_t i=0; i<5; i++)
  // {
  //   char check[8];
  //   sprintf(check, "%d", bufl[i]);
  //   OLED_ShowStr(40,4,check,2);
  //   HAL_Delay(1000);
  //   OLED_CLS();
  // }

  OLED_Init();			//��ʼ��OLED    
	
  HAL_TIM_Base_Start_IT(&htim6);
  KEYBRD_Init();

  int8_t keypad_state[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

  struct KEYBRD_INFO keyboard_info = {{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},0,0};
  
  

  uint8_t main_state = 0;
  uint32_t count = 0;

  HAL_Delay(2000);
  OLED_CLS();

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
    // OLED_CLS();
		// HAL_Delay(500);
    // OLED_ShowStr(40,6," Ver 1.2  ",2);
		// // num ++;
    // // OLED_ShowNum(40,2,num,4,2);
    // HAL_Delay(50);

    int8_t last_display = keyboard_info.display_answer;

    // 键盘读取
    if (KEYBRD_Read_En)
    {
      KEYBRD_Read(KEYBRD_Read_Row, keyboard_info.keypad_state);
    }
    // 键盘处理读取到的状态
    uint8_t next_state = KEYBRD_get_func(&keyboard_info, main_state);

    switch (main_state)
    {
    case 0:
      // 等待键盘输入
      UI_default(&keyboard_info,0);
      break;
    
    case 1:
      // 已获得输入，等待发送
      UI_default(&keyboard_info,0);
      break;

    case 2:
      // 发送中
      UI_default(&keyboard_info,1);

      // OLED_ShowNum(10,0,1,4,2);
      tx_data[0] = keyboard_info.current_answer + 64;
      // nrf24l01p_tx_transmit(tx_data);
      // 发送数据
      uint8_t tr = 0;
      // while (tr != 46 || tr != 30 || tr != 31)
      // {
        
      //   HAL_Delay(5);
      // }

      tr = nrf24l01p_write_tx_fifo(tx_data);
      nrf24l01p_clear_rx_dr();
      nrf24l01p_clear_tx_ds();
      nrf24l01p_clear_max_rt();
      // HAL_Delay(500);
      OLED_CLS();
      // tr = nrf24l01p_write_tx_fifo(tx_data);
      // OLED_ShowNum(10,4,tr,4,2);

      // 发送成功运行
      

      next_state = 0;
      break;

    case 3:
      // 
      UI_default(&keyboard_info,0);
      // OLED_ShowNum(10,6,2,4,2);
      break;

    default:
      UI_default(&keyboard_info,0);
      break;
    }
    
    if(main_state != next_state || last_display != keyboard_info.display_answer){
      OLED_CLS();
    }
    main_state = next_state;

    if (keypad_state[6] == -1)
    {
      OLED_CLS();
      // HAL_Delay(50);
    }
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
