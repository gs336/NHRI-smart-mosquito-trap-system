function varargout = Camera_Platform(varargin)
% CAMERA_PLATFORM MATLAB code for Camera_Platform.fig
%      CAMERA_PLATFORM, by itself, creates a new CAMERA_PLATFORM or raises the existing
%      singleton*.
%
%      H = CAMERA_PLATFORM returns the handle to a new CAMERA_PLATFORM or the handle to
%      the existing singleton*.
%
%      CAMERA_PLATFORM('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CAMERA_PLATFORM.M with the given input arguments.
%
%      CAMERA_PLATFORM('Property','Value',...) creates a new CAMERA_PLATFORM or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Camera_Platform_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Camera_Platform_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Camera_Platform

% Last Modified by GUIDE v2.5 12-Dec-2018 16:06:54

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Camera_Platform_OpeningFcn, ...
                   'gui_OutputFcn',  @Camera_Platform_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT

% --- Executes just before Camera_Platform is made visible.
function Camera_Platform_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Camera_Platform (see VARARGIN)

% Choose default command line output for Camera_Platform
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
% UIWAIT makes Camera_Platform wait for user response (see UIRESUME)
% uiwait(handles.figure1);
global Arduino;
global typ;
global lights;
global Cam_Ang;
global Plate_Ang;
global Mycam;
global Sex;
Sex = 'M';
Cam_Ang=0;
Plate_Ang=0;
typ = 'A';
lights = 0;

delete(instrfindall);
%Arduino=serial('COM6','BaudRate',9600);
Arduino=serial('COM3','BaudRate',9600);
fopen(Arduino);
Mycam = webcam(1);
%Mycam.Exposure=-5;
imshow('logo3.png','Parent',handles.axes_Name);
axis image;
%handles.axes_Name = imshow('logo_gray.jpg');
%handles.axes_Name = imshow('title.png');


%set(handles.axes_Name,'Units','pixels');
%resizePos = get(handles.axes_Name,'Position');
%myImage= imresize(myImage, [resizePos(3) resizePos(3)]);
%axes(handles.axes_Name);
%imshow(myImage);
%set(handles.axes_Name,'Units','normalized');

%ax = axes('Parent', handles.axes1, 'Units', 'normalized', 'Position', [0 0 1 1]);
camsize = str2double( strsplit(Mycam.Resolution, 'x'));
im = image('Parent', handles.axes1);
preview(Mycam, im); 






% --- Outputs from this function are returned to the command line.
function varargout = Camera_Platform_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in Cam_Shot.
function Cam_Shot_Callback(hObject, eventdata, handles)
% hObject    handle to Cam_Shot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global Arduino;
    global typ;
    global lights;
    global Mycam;
    global Cam_Ang;
    global Plate_Ang;
    global Sex;
    Data = 'dd';
    fprintf(Arduino,Data);
    pause(3);
    %control LED lights
    %lights = get(handles.LED_Slider,'Value');

    %shot at all angle in zero 
    %Cam_Ang;
    Lighting  = 1;
    CamStep = 0;
    PlateStep = 0;
    if (get(handles.LED_Slider,'Value'))==0
        LightingLimit = 1;
    else
        LightingLimit = 10;
    end
    
    if (get(handles.CamMotor_Slider,'Value'))==0
       CamStepLimit = 0;
    else
        CamStepLimit = 85;
    end
    if (get(handles.PlateMotor_Slider, 'Value'))==0
       PlateStepLimit = 1;
    else
       PlateStepLimit = 200;
    end
    Save_Address =strcat('Pic\',typ,'_',Sex,'\');%%Path of Save Picture
    if ~exist(Save_Address,'dir')
        mkdir(Save_Address); 
    end
    while CamStep<=CamStepLimit
%control camera's motor
%shot angle in 0/0
       %Save_Address ='C:\Users\Liu\Desktop\NHRI\Matlab\Pic\';
        %Pic_Path = strcat(Save_Address,typ,'_light',num2str(lights),'_CamAng',num2str(Cam_Ang),...
        %'_PlateAng',num2str(Plate_Ang),'.jpg');
      %  img = snapshot(Mycam);
        %imwrite(img,Pic_Path);
       % pause(3);
        set(handles.CamAngText,'String',strcat('Cam Angle:',num2str(Cam_Ang)));
        
        while PlateStep<PlateStepLimit
            set(handles.PlateAngText,'String',strcat('Plate Angle:',num2str(Plate_Ang)));
            while Lighting<=LightingLimit
                val = Lighting-1;
                Data =strcat('a',num2str(val));
                fprintf(Arduino,Data);
                pause(0.3);
                Save_Address =strcat('Pic\',typ,'_',Sex,'\');%%Path of Save Picture
                %if ~exist(Save_Address,'dir') 
                    %mkdir(Save_Address); 
                %end
                Pic_Path = strcat(Save_Address,'_camAng_',num2str(CamStep),'_lighting_',num2str(Lighting),...
                '_angle_',num2str(PlateStep),'.JPEG');
                while ~exist(Pic_Path,'file')
                    img = snapshot(Mycam);
                    imwrite(img,Pic_Path);
                end
                    
                    set(handles.text12,'String',strcat(Pic_Path,'    saved'));
                    %lights = get(handles.LED_Slider,'Value');
                    %else
                    Lighting = Lighting + round(get(handles.LED_Slider,'Value'));
                    %val = Lighting-1;
                    %if(val==-1)
                        %Data='a/';
                    %Data =strcat('a',num2str(val));
                    %end
                    %fprintf(Arduino,Data);
            end
            Lighting = 1;
            %%control Plate's motor
            val = round(get(handles.PlateMotor_Slider,'Value'))-1;
            if(val==-1)
                Data='c/';
            else
                Data =strcat('c',num2str(val));
            end
            PlateStep = PlateStep + round(get(handles.PlateMotor_Slider,'Value'));
            Plate_Ang = Plate_Ang + 1.8*(round(get(handles.PlateMotor_Slider,'Value')));
            fprintf(Arduino,Data);
            pause(0.3);
           
            %imshow(img);
            %lights = set(handles.LED_Light,'String',);
            %filename=strcat(f1, 'lighting_' ,int2str(i),'angle_', int2str(num),'.JPEG'); 

            %filename = strcat('DataFile/',typ,'_',gen,'/_camAng_',camAng, ...
            %'_lighting_',lights,'_angle_',mosAng,'.JPEG');
            %filename1 = strcat('1','.jpg');    
            %preview(Mycam);
            
        end
        Plate_Ang=0;
        PlateStep = 0;
        %Data ='dd';
        %fprintf(Arduino,Data);
        %pause(3);
        %%control Camera's motor
        val = round(get(handles.CamMotor_Slider,'Value'))-1;
        if(val==-1)
            Data='b/';
        else
            Data =strcat('b',num2str(val));
        end
        CamStep = CamStep + round(get(handles.PlateMotor_Slider,'Value'));
        fprintf(Arduino,Data);
        Cam_Ang = Cam_Ang + 1.8*(round(get(handles.CamMotor_Slider,'Value')));
        %pause(0.5);
    end
    %%return to zero
    Data ='dd';
    fprintf(Arduino,Data);
    %pause(3);
    Plate_Ang=0;
    Cam_Ang=0;
    %clear('Mycam');


% --- Executes on slider movement.
function LED_Slider_Callback(hObject, eventdata, handles)
% hObject    handle to LED_Slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    %val = strcat(handles.LED_Slider);
    
    Max=10;Min=0;
    set(hObject,'SliderStep',[1/(Max-Min) 1/(Max-Min)]);
    val = strcat('Value : ',num2str(round(get(handles.LED_Slider, 'Value'))));
    set(handles.LED_Val,'String', val);
    

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function LED_Slider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to LED_Slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function CamMotor_Slider_Callback(hObject, eventdata, handles)
% hObject    handle to CamMotor_Slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
    Max=10;Min=0;
    set(hObject,'SliderStep',[1/(Max-Min) 1/(Max-Min)]);
    val = strcat('Value : ',num2str(round(get(handles.CamMotor_Slider, 'Value'))));
    set(handles.CamMotor_Val,'String', val);


% --- Executes during object creation, after setting all properties.
function CamMotor_Slider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to CamMotor_Slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function PlateMotor_Slider_Callback(hObject, eventdata, handles)
% hObject    handle to PlateMotor_Slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
    Max=10;Min=0;
    set(hObject,'SliderStep',[1/(Max-Min) 1/(Max-Min)]);
    val = strcat('Value : ',num2str(round(get(handles.PlateMotor_Slider, 'Value'))));
    set(handles.PlateMotor_Val,'String', val);

% --- Executes during object creation, after setting all properties.
function PlateMotor_Slider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PlateMotor_Slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on selection change in Type_Menu.
function Type_Menu_Callback(hObject, eventdata, handles)
% hObject    handle to Type_Menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns Type_Menu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from Type_Menu
global typ;
contents_all = get(hObject,'String');
contents = get(hObject,'Value');
%typ = contents{1};
switch contents
    case 1
        %set(handles.text12,'String',contents_all{1});
        %typ = contents_all{1};
        typ = 'A';
    case 2
        %set(handles.text12,'String',contents_all{2});
        %typ = contents_all{2};
        typ = 'C';
end
        

% --- Executes during object creation, after setting all properties.
function Type_Menu_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Type_Menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in Sexuality_Menu.
function Sexuality_Menu_Callback(hObject, eventdata, handles)
% hObject    handle to Sexuality_Menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns Sexuality_Menu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from Sexuality_Menu
global Sex;
contents_all = get(hObject,'String');
contents = get(hObject,'Value');
%typ = contents{1};
switch contents
    case 1
        %set(handles.text12,'String',contents_all{1});
        %Sex = contents_all{1};
        Sex = 'M';
    case 2
        %set(handles.text12,'String',contents_all{2});
        %Sex = contents_all{2};
        Sex = 'F';
end


% --- Executes during object creation, after setting all properties.
function Sexuality_Menu_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Sexuality_Menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes when user attempts to close figure1.
function figure1_CloseRequestFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global Mycam;
global Arduino;
close(Mycam);
closePreview(Mycam);
fclose(Arduino);
delete(instrfindall);
clear;
%close(handles.figure1);
% Hint: delete(hObject) closes the figure
delete(hObject);
