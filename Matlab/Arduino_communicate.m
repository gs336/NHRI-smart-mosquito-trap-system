delete(instrfindall);
Arduino=serial('COM16','BaudRate',9600);
%val = '';
%    fopen(Arduino);
 %   fprintf(Arduino,'%c',val);
%fprintf(Arduino,255);

%a = arduino('COM10','micro');%matlab concontrol arduino
%readVoltage(a,'A0');

fclose(Arduino);
delete(instrfindall);