package temp;
import java.util.Scanner;

class Levenshtein{
    public static void main(String args[]){
        Scanner read = new Scanner(System.in);

        System.out.print("Enter two strings: ");
        String string1 = read.nextLine();
        String string2 = read.nextLine();

        read.close();

        System.out.println("Edit distance: " + Integer.toString(levenshtein_accuracy(string1, string2)));
    };

    static int levenshtein_accuracy(String a, String b){
        // considering a -> b

        //checking whether one of them is empty
        if(a.length() == 0 || b.length() == 0) return Math.max(a.length(), b.length());

        // Creating the grid
        int[][] dp = new int[a.length() + 1][b.length() + 1];

        // inserting values for first row and column.
        for(int i = 0; i <= a.length(); i++) dp[i][0] = i;
        for(int i = 0; i <= b.length(); i++) dp[0][i] = i;

        // inserting values for the rest of the grid
        for(int i = 1; i <= a.length(); i++){
            for(int j = 1; j <= b.length(); j++){
                if(a.charAt(i-1) == b.charAt(j-1)) dp[i][j] = dp[i-1][j-1];
                else dp[i][j] = 1 + Math.min(dp[i-1][j-1], Math.min(dp[i-1][j], dp[i][j-1]));
            };
        };

        // printing the grid to verify
        // for(int i = 0; i < dp.length; i++){
        //     for(int j = 0; j < dp[i].length; j++) System.out.print(dp[i][j] + " ");
        //     System.out.println();
        // };

        return dp[a.length()][b.length()];
    };
};