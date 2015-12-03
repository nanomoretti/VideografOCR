#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <iostream>


using namespace cv;

/// Global variables

int threshold_value = 0;
int threshold_type = 3;;
int const max_value = 255;
int const max_type = 4;
int const max_BINARY_value = 255;

Mat src, src_gray, dst;
char* window_name = "Threshold Demo";

char* trackbar_type = "Type: \n 0: Binary \n 1: Binary Inverted \n 2: Truncate \n 3: To Zero \n 4: To Zero Inverted";
char* trackbar_value = "Value";

/// Function headers
void Threshold_Demo( int, void* );

Point point1, point2; /*vertical points of the bounding box*/
int drag = 0;
Rect rect; /*bounding box*/
Mat img, roiImg,dilation_dst; /* roiImg - the part of the image in the bounding box */
int select_flag = 0;

std::string exec(const char* cmd) {
    FILE* pipe = popen(cmd, "r");
    if (!pipe) return "ERROR";
    char buffer[128];
    std::string result = "";
    while (!feof(pipe)) {
        if (fgets(buffer, 128, pipe) != NULL)
            result += buffer;
    }
    pclose(pipe);
    return result;
}


void mouseHandler(int event, int x, int y, int flags, void* param)
{
    if (event == CV_EVENT_LBUTTONDOWN && !drag)
    {
        /*left button clicked. ROI selection begins*/
        point1 = Point(x, y);
        drag = 1;
    }
     
    if (event == CV_EVENT_MOUSEMOVE && drag)
    {
        /*mouse dragged. ROI being selected*/
        Mat img1 = dst.clone();
        point2 = Point(x, y);
        rectangle(img1, point1, point2, CV_RGB(255, 0, 0), 3, 8, 0);
        imshow(window_name, img1);
    }
     
    if (event == CV_EVENT_LBUTTONUP && drag)
    {
        point2 = Point(x, y);
        rect = Rect(point1.x,point1.y,x-point1.x,y-point1.y);
        drag = 0;
        roiImg = dst(rect);
    }
     
    if (event == CV_EVENT_LBUTTONUP)
    {
       /*ROI selected*/
        select_flag = 1;
        drag = 0;
    }
}



/**
 * @function main
 */
int main( int argc, char** argv )
{
  
  char* ImagenesXesperado[4][2] = {
    "1.jpeg","Negociaciones en La Habana Colombia cerca de la paz luego de 3 años",
	"2.jpeg","Festival Raíz Tecnópolis Así se hace el salteado patagónico",
	"3.jpeg","Todos jugaron para Boca Lo mejor y lo peor de la fecha",
	"4.jpeg","Bebés que se chupan el dedo"};
  int i=0;
  src=imread(ImagenesXesperado[0][0], CV_LOAD_IMAGE_COLOR); 
  
 
  /// Convert the image to Gray
  cvtColor( src, src_gray, CV_BGR2GRAY );

  /// Create a window to display results
  namedWindow( window_name, CV_WINDOW_AUTOSIZE );

  /// Create Trackbar to choose type of Threshold
  createTrackbar( trackbar_type,
                  window_name, &threshold_type,
                  max_type, Threshold_Demo );

  createTrackbar( trackbar_value,
                  window_name, &threshold_value,
                  max_value, Threshold_Demo );

  /// Call the function to initialize
  Threshold_Demo( 0, 0 );

  /// Wait until user finishes program
  while(true)
  {
    int c;
    cvtColor( src, src_gray, CV_BGR2GRAY );
    cvSetMouseCallback(window_name, mouseHandler, NULL);
    Threshold_Demo( 0, 0 );
    c = waitKey( 20 );
    if (select_flag == 1)
    {
        bilateralFilter ( roiImg, dilation_dst, 1, 1*2, 1/2 );
  		imshow("ROI", dilation_dst); /*show the image bounded by the box*/
    }
    
    if (c == 114 && select_flag == 1)
    {
      imwrite("roiImg.jpg", dilation_dst);
      system("tesseract roiImg.jpg stdout -l spa >> log.txt");
      std::cout << exec("tesseract roiImg.jpg stdout -l spa");  
    }

    if (c == 115)
    { 
    	 i=(i+1)%4;
         src=imread(ImagenesXesperado[i][0], CV_LOAD_IMAGE_COLOR); 
    }
    
    if(c==27 )
    { 
    	break; 
    }
    rectangle(dst, rect, CV_RGB(255, 0, 0), 3, 8, 0);
    imshow(window_name, dst);
   }

}


/**
 * @function Threshold_Demo
 */
void Threshold_Demo( int, void* )
{
  /* 
  	 0: Binary
     1: Binary Inverted
     2: Threshold Truncated
     3: Threshold to Zero
     4: Threshold to Zero Inverted
  */

  threshold( src_gray, dst, threshold_value, max_BINARY_value,threshold_type );
  //rectangle(dst, rect, CV_RGB(255, 0, 0), 3, 8, 0);
  //imshow(window_name, dst);
  
}
