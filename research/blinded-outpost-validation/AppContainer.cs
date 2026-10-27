// SPDX-License-Identifier: GPL-3.0-or-later
// Original offline launcher. Windows SDK ABI declarations only; no game APIs.
// Creates a disposable capability-free profile; caller grants its SID access
// only to provisioned files. No elevation, account creation or network grant.
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;

public static class BlindContainer {
    [StructLayout(LayoutKind.Sequential)] struct SI {
        public int cb; public IntPtr reserved, desktop, title;
        public int x,y,xs,ys,xc,yc,fill,flags; public short show,reserved2;
        public IntPtr reserved3, input, output, error;
    }
    [StructLayout(LayoutKind.Sequential)] struct SIX { public SI si; public IntPtr attributes; }
    [StructLayout(LayoutKind.Sequential)] struct PI { public IntPtr process,thread; public int pid,tid; }
    [StructLayout(LayoutKind.Sequential)] struct CAP { public IntPtr sid, capabilities; public int count,reserved; }
    [DllImport("userenv.dll", CharSet=CharSet.Unicode)] static extern int CreateAppContainerProfile(
        string name,string display,string description,IntPtr capabilities,int count,out IntPtr sid);
    [DllImport("userenv.dll", CharSet=CharSet.Unicode)] static extern int DeleteAppContainerProfile(string name);
    [DllImport("advapi32.dll", CharSet=CharSet.Unicode, SetLastError=true)] static extern bool ConvertSidToStringSid(IntPtr sid,out IntPtr text);
    [DllImport("kernel32.dll")] static extern IntPtr LocalFree(IntPtr p);
    [DllImport("advapi32.dll")] static extern IntPtr FreeSid(IntPtr p);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool InitializeProcThreadAttributeList(
        IntPtr list,int count,int flags,ref IntPtr size);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool UpdateProcThreadAttribute(
        IntPtr list,int flags,IntPtr attribute,IntPtr value,IntPtr size,IntPtr previous,IntPtr returned);
    [DllImport("kernel32.dll")] static extern void DeleteProcThreadAttributeList(IntPtr list);
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)] static extern bool CreateProcess(
        string exe,System.Text.StringBuilder cmd,IntPtr pa,IntPtr ta,bool inherit,int flags,
        IntPtr environment,string cwd,ref SIX si,out PI pi);
    [DllImport("kernel32.dll")] static extern int WaitForSingleObject(IntPtr handle,int milliseconds);
    [DllImport("kernel32.dll")] static extern bool GetExitCodeProcess(IntPtr process,out int code);
    [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr handle);
    [DllImport("advapi32.dll", SetLastError=true)] static extern bool OpenProcessToken(IntPtr p,int access,out IntPtr token);
    [DllImport("advapi32.dll", SetLastError=true)] static extern bool GetTokenInformation(
        IntPtr token,int kind,IntPtr data,int size,out int needed);
    [DllImport("advapi32.dll")] static extern bool EqualSid(IntPtr a,IntPtr b);
    [DllImport("kernel32.dll")] static extern uint ResumeThread(IntPtr thread);
    [DllImport("kernel32.dll")] static extern bool TerminateProcess(IntPtr process,int code);
    static IntPtr sid = IntPtr.Zero;
    public static bool ProfileCreated = false;
    public static int ProfileResult = 0;
    public static bool TokenVerified = false;
    public static string Create(string name) {
        int result=CreateAppContainerProfile(name,name,"Disposable SOR offline qualification",IntPtr.Zero,0,out sid);
        ProfileResult=result; ProfileCreated=result>=0;
        if(result<0) Marshal.ThrowExceptionForHR(result);
        IntPtr text;
        if(!ConvertSidToStringSid(sid,out text)) throw new Win32Exception();
        try { return Marshal.PtrToStringUni(text); } finally { LocalFree(text); }
    }
    public static int Run(string exe,string arguments,string cwd) {
        IntPtr size=IntPtr.Zero;
        InitializeProcThreadAttributeList(IntPtr.Zero,1,0,ref size);
        IntPtr attrs=Marshal.AllocHGlobal(size);
        CAP caps=new CAP(); caps.sid=sid;
        IntPtr value=Marshal.AllocHGlobal(Marshal.SizeOf(caps));
        bool initialized=false;
        try {
            if(!InitializeProcThreadAttributeList(attrs,1,0,ref size)) throw new Win32Exception();
            initialized=true; Marshal.StructureToPtr(caps,value,false);
            if(!UpdateProcThreadAttribute(attrs,0,new IntPtr(0x20009),value,
                    new IntPtr(Marshal.SizeOf(caps)),IntPtr.Zero,IntPtr.Zero)) throw new Win32Exception();
            SIX startup=new SIX(); startup.si.cb=Marshal.SizeOf(startup); startup.attributes=attrs;
            PI pi;
            if(!CreateProcess(exe,new System.Text.StringBuilder("\""+exe+"\" "+arguments),
                    IntPtr.Zero,IntPtr.Zero,false,0x80000|0x08000000|4,IntPtr.Zero,cwd,ref startup,out pi))
                throw new Win32Exception();
            try {
                IntPtr token=IntPtr.Zero, info=Marshal.AllocHGlobal(4096);
                try {
                    int needed;
                    if(!OpenProcessToken(pi.process,8,out token)) throw new Win32Exception();
                    if(!GetTokenInformation(token,29,info,4096,out needed) || Marshal.ReadInt32(info)!=1)
                        throw new InvalidOperationException("Child is not an AppContainer");
                    if(!GetTokenInformation(token,31,info,4096,out needed) || !EqualSid(Marshal.ReadIntPtr(info),sid))
                        throw new InvalidOperationException("Unexpected child AppContainer SID");
                    if(!GetTokenInformation(token,30,info,4096,out needed) || Marshal.ReadInt32(info)!=0)
                        throw new InvalidOperationException("Unexpected child capabilities");
                    TokenVerified=true;
                } finally { if(token!=IntPtr.Zero) CloseHandle(token); Marshal.FreeHGlobal(info); }
                if(ResumeThread(pi.thread)==0xffffffff) throw new Win32Exception();
                // Offline fixture completion only; no scientific target deadline.
                WaitForSingleObject(pi.process,-1);
                int code; if(!GetExitCodeProcess(pi.process,out code)) throw new Win32Exception();
                return code;
            } catch { TerminateProcess(pi.process,125); throw; }
            finally { CloseHandle(pi.thread); CloseHandle(pi.process); }
        } finally {
            if(initialized) DeleteProcThreadAttributeList(attrs);
            Marshal.FreeHGlobal(value); Marshal.FreeHGlobal(attrs);
        }
    }
    public static void Delete(string name) {
        if(sid!=IntPtr.Zero) { FreeSid(sid); sid=IntPtr.Zero; }
        if(ProfileCreated) {
            int result=DeleteAppContainerProfile(name); if(result<0) Marshal.ThrowExceptionForHR(result);
        }
    }
}
