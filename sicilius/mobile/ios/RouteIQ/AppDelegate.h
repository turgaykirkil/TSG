#import <RCTAppDelegate.h>
#import <UIKit/UIKit.h>
#import <React/RCTBridgeDelegate.h>

@interface AppDelegate : RCTAppDelegate

@property (nonatomic, strong) UIWindow *window;
@property (nonatomic, strong) NSDictionary *initialProps;

@end
